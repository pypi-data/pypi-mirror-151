""""""
import multiprocessing
import queue

from .exceptions import SignalBotError



class GeneralHandler:
    """"""
    def __init__(self, func, args=None, kwargs=None):
        """"""
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}

    def run(self, obj):
        """"""
        return self.func(obj, *self.args, **self.kwargs)

    def run_async(self, obj):
        """"""
        multiprocessing.Process(target=self.func, args=[obj, *self.args],
                                kwargs=self.kwargs).start()


class MessageHandler(GeneralHandler):
    """"""
    def __init__(self, func, messagefilter=None, args=None, kwargs=None):
        """"""
        super().__init__(func, args, kwargs)
        self.filter = messagefilter

    def run(self, obj):
        """"""
        if self.match_filter(obj) is True:
            super().run(obj)

    def run_async(self, obj):
        """"""
        if self.match_filter(obj) is True:
            super().run_async(obj)

    def match_filter(self, message):
        """"""
        return self.filter is None or self.filter.check(message)


class OriginHandler(GeneralHandler):
    """"""
class ErrorHandler(GeneralHandler):
    """"""
class ExceptionHandler(GeneralHandler):
    """"""
class PayloadHandler(GeneralHandler):
    """"""


class ConversationHandler:
    """"""
    PREDEFINED_STATES = ["end"]

    def __init__(self, states, entryhandler, aborthandler=None,
                 endhandler=None, timeouthandler=None, timeout=600,
                 groupconversation=False, exclusive=True):
        """"""
        self.states = states
        self.entryhandler = entryhandler
        self.aborthandler = aborthandler
        self.endhandler = endhandler
        self.timeouthandler = timeouthandler
        self.timeout = timeout
        self.groupconversation = groupconversation
        self.exclusive = exclusive

    def is_entry(self, message):
        """"""
        return self.entryhandler.match_filter(message)

    def handle_entry(self, message):
        """"""
        result = self.entryhandler.run(message)
        self.validate_state(result)
        return result

    def handle_timeout(self, origin):
        """"""
        if self.timeouthandler is not None:
            self.timeouthandler.run(origin)

    def handle_end(self, origin):
        """"""
        if self.endhandler is not None:
            self.endhandler.run(origin)

    def handle_message(self, state, message):
        """"""
        if self.aborthandler is not None \
                and self.aborthandler.run(message) is not False:
            return "ended"
        if state in self.states:
            for handler in self.states[state]:
                result = handler.run(message)
                if result is not False:
                    self.validate_state(result)
                    return result
        return state

    def validate_state(self, state):
        """"""
        if state not in self.states and state not in self.PREDEFINED_STATES:
            raise SignalBotError(f"Undefined conversation state '{state}' " \
                                 "returned by handler!")



class Conversation:
    """"""
    def __init__(self, message, convhandler):
        """"""
        self.entrymessage = message
        self.convhandler = convhandler
        self.messagequeue = multiprocessing.Queue()
        self.state = None
        self.process = multiprocessing.Process(target=self.enter)

    def run_async(self):
        """"""
        self.process.start()

    def running(self):
        """"""
        return self.process.is_alive()

    def enter(self):
        """"""
        self.state = self.convhandler.handle_entry(self.entrymessage)
        while True:
            if self.state == "end":
                self.convhandler.handle_end(self.entrymessage.origin)
                self.state = "ended"
            if self.state == "ended":
                return
            try:
                message = self.messagequeue.get(
                    timeout=self.convhandler.timeout)
            except queue.Empty:
                self.state = "timeout"
                self.convhandler.handle_timeout(self.entrymessage.origin)
                self.state = "ended"
                return
            self.state = self.convhandler.handle_message(self.state, message)
