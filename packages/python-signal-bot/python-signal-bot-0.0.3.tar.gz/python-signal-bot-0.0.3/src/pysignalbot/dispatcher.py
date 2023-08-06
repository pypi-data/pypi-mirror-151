""""""
import ctypes
import json
import logging
import multiprocessing
import select
import socket
import time

from .exceptions import DispatcherError, SocketError
from .handlers import (Conversation, ConversationHandler, ErrorHandler,
                       ExceptionHandler, MessageHandler, PayloadHandler)
from .models import (DataMessage, ErrorResponse, Message, MessageResponse,
                     PrettyNamespace, ReceiptMessage, Response, ReceiveError,
                     TypingMessage)

class Dispatcher:
    """"""
    def __init__(self, signalcli_host, signalcli_port):
        """"""
        self.log = logging.getLogger(__name__)
        self.signalcli_host = signalcli_host
        self.signalcli_port = signalcli_port
        self.signalcli_socket = None
        self.payloadhandlers = []
        self.messagehandlers = []
        self.conversationhandlers = []
        self.errorhandlers = []
        self.exceptionhandlers = []
        self.conversations = {}
        self.async_process = None
        manager = multiprocessing.Manager()
        self.responses = manager.dict()
        self.connected = manager.Value(ctypes.c_bool, False)

    def exit(self):
        """"""
        if self.connected.value is True:
            self.disconnect()
            if self.async_process is not None:
                self.async_process.terminate()

    def disconnect(self):
        """"""
        if self.connected.value is True:
            self.signalcli_socket.shutdown(socket.SHUT_RDWR)
            self.signalcli_socket.close()
            self.connected.value = False

    def connect(self, retry_backoff=True):
        """"""
        tries = 1
        while self.connected.value is False:
            try:
                self.signalcli_socket = socket.socket(socket.AF_INET,
                                                      socket.SOCK_STREAM)
                self.signalcli_socket.connect((self.signalcli_host,
                                               self.signalcli_port))
                self.signalcli_socket.setblocking(False)
                self.connected.value = True
            except (ConnectionRefusedError, OSError) as exc:
                if retry_backoff is False:
                    raise exc
                if tries > 30:
                    raise SocketError(f"Socket connection failed to often!") \
                        from exc
                wait = tries * 2
                self.log.error("Socket connection failed, waiting %s " \
                                 "seconds and retrying...", wait)
                time.sleep(wait)
                tries += 1
        self.log.info("Socket connected!")

    def run(self):
        """"""
        if self.connected.value is False:
            self.connect()
        while True:
            try:
                self.wait_and_handle()
            except SocketError as exc:
                self.log.info("Socket connection error! Reconnecting...")
                self.disconnect()
                self.connect()
            except Exception as exc:
                self.dispatch_exception(exc)

    def run_async(self):
        """"""
        if self.connected.value is False:
            self.connect()
        self.async_process = multiprocessing.Process(target=self.run)
        self.async_process.start()

    def wait_and_handle(self):
        """"""
        chunks = []
        while True:
            readable, _, _ = select.select([self.signalcli_socket], [], [], 60)
            if len(readable) > 0:
                chunk = self.signalcli_socket.recv(1024)
                if len(chunk) == 0:
                    raise SocketError("Socket is disconnected!")
                chunks.append(chunk)
                if len(chunk) > 0 and chunk[-1] == 10:
                    payload = b"".join(chunks)
                    for payload in payload.strip().split(b"\n"):
                        self.dispatch_payload(payload)
                    break

    def add(self, handlers):
        """"""
        if not isinstance(handlers, list):
            handlers = [handlers]
        for handler in handlers:
            if isinstance(handler, PayloadHandler):
                self.payloadhandlers.append(handler)
            elif isinstance(handler, MessageHandler):
                self.messagehandlers.append(handler)
            elif isinstance(handler, ConversationHandler):
                self.conversationhandlers.append(handler)
            elif isinstance(handler, ErrorHandler):
                self.errorhandlers.append(handler)
            elif isinstance(handler, ExceptionHandler):
                self.exceptionhandlers.append(handler)
            else:
                raise DispatcherError("Invalid handler type!")

    def send(self, payload):
        """"""
        self.signalcli_socket.sendall(bytes(f"{json.dumps(payload)}\n",
                                            encoding="utf-8"))

    def dispatch_payload(self, raw_payload):
        """"""
        try:
            payload_dict = json.loads(raw_payload)
        except json.decoder.JSONDecodeError as exc:
            raise DispatcherError("Payload with invalid JSON: " \
                                  f"{raw_payload}") from exc
        payload = json.loads(raw_payload,
                             object_hook=lambda dct: PrettyNamespace(**dct))
        for handler in self.payloadhandlers:
            handler.run_async(payload)
        if "error" in payload_dict and "id" in payload_dict:
            self.responses[payload.id] = ErrorResponse(payload)
            return
        if "result" in payload_dict:
            if "results" in payload_dict["result"]:
                self.responses[payload.id] = MessageResponse(payload)
            else:
                self.responses[payload.id] = Response(payload)
        elif "method" in payload_dict and payload.method == "receive":
            if "exception" in payload_dict["params"]:
                self.dispatch_error(ReceiveError(payload.params))
            else:
                envelope_dict = payload_dict["params"]["envelope"]
                if "receiptMessage" in envelope_dict:
                    message = ReceiptMessage(payload.params)
                elif "typingMessage" in envelope_dict:
                    message = TypingMessage(payload.params)
                elif "dataMessage" in envelope_dict:
                    message = DataMessage(payload.params)
                else:
                    message = Message(payload.params)
                self.dispatch_message(message)

    def dispatch_message(self, message):
        """"""
        stop_dispatching = False
        if isinstance(message, DataMessage):
            self.cleanup_conversations()
            conversation = self.conversations.get(message.origin)
            if conversation is not None:
                conversation.messagequeue.put(message)
                stop_dispatching = conversation.convhandler.exclusive
            elif len(message.origin) == 2:
                conversation = self.conversations.get(message.origin[:1])
                if conversation is not None \
                        and conversation.convhandler.groupconversation is True:
                    conversation.messagequeue.put(message)
                    stop_dispatching = conversation.convhandler.exclusive
            else:
                for convhandler in self.conversationhandlers:
                    if convhandler.is_entry(message) is True:
                        conversation = Conversation(message, convhandler)
                        origin = message.origin
                        if convhandler.groupconversation is True \
                                and len(origin) == 2:
                            origin = origin[:1]
                        self.conversations[origin] = conversation
                        conversation.run_async()
                        stop_dispatching = convhandler.exclusive
                        break
        if stop_dispatching is False:
            for handler in self.messagehandlers:
                handler.run_async(message)

    def cleanup_conversations(self):
        """"""
        remove = []
        for origin, conversation in self.conversations.items():
            if conversation.running() is False:
                remove.append(origin)
        for origin in remove:
            self.conversations.pop(origin)

    def dispatch_error(self, error):
        """"""
        for handler in self.errorhandlers:
            handler.run_async(error)

    def dispatch_exception(self, exc):
        """"""
        for handler in self.exceptionhandlers:
            handler.run(exc)
