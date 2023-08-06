""""""
import glob
import json
import os
import re
import time
import uuid

from .dispatcher import Dispatcher
from .exceptions import (GroupSendError, RpcCallError, RpcCallTimeoutError,
                         SendError, SignalBotError)
from .models import (DataMessage, ErrorResponse, PrettyNamespace, Response,
                     SendAttachment, Stickerpack)

# TODO
# - Check Untrusted Group Member Send

# Might implement in the future:
# - Operations on profile, group, contacts and configuration; blocking
# - Some kind of script for registration and verification

# Not working/not implemented/undocumented in signal-cli:
# - Quoting message with sticker/image won't show sticker/image thumbnail in the quote
# - Quoting image/sticker only message will lead to no quote at all
# - Sending images with "view once"
# - Sometimes the about_emoji seems to get set in a weird way when using update_profile


class Bot:
    """"""
    def __init__(self, signalcli_host, signalcli_port, signalcli_data="/data",
                 local_data="/data"):
        """"""
        self.signalcli_host = signalcli_host
        self.signalcli_port = int(signalcli_port)
        self.signalcli_data = signalcli_data
        self.local_data = local_data
        self.stickerpacks = []
        self.refresh_stickerpacks()
        self.dispatcher = None

    def __enter__(self):
        """"""
        self.dispatcher = Dispatcher(self.signalcli_host, self.signalcli_port)
        return self

    def __exit__(self, *args):
        """"""
        self.dispatcher.exit()

    def rpc_call(self, method, params=None, timeout=5, delay=0.3):
        """"""
        request_id = str(uuid.uuid4())
        payload = {"jsonrpc":"2.0", "method":method, "params":params,
                   "id":request_id}
        self.dispatcher.send(payload)
        schedule = [*([delay] * int(timeout // delay)), timeout % delay]
        for seconds in schedule:
            time.sleep(seconds)
            try:
                response = self.dispatcher.responses.pop(request_id)
                break
            except KeyError:
                pass
        else:
            raise RpcCallTimeoutError("Timeout while waiting for response; " \
                                      f"call payload: {payload}")
        if isinstance(response, ErrorResponse):
            try:
                error_type = response.data.response.results[0].type
                if error_type in ("UNREGISTERED_FAILURE", "IDENTITY_FAILURE"):
                    raise SendError("Sending to recipient failed!",
                                    response.data.response.results)
            except (AttributeError, IndexError):
                pass
            try:
                if "User is not a member in group" in response.message \
                        or "Invalid group id" in response.message \
                        or "Group not found" in response.message:
                    raise GroupSendError("Sending to group failed!",
                                         response)
            except (AttributeError, TypeError):
                pass

            raise RpcCallError("Calling failed with error!", response)
        try:
            for result in response.result.results:
                if result.type != "SUCCESS":
                    raise SendError("Sending failed for some recipients!",
                                    response.result.results)
        except AttributeError:
            pass
        return response

    def send_message(self, recipient, text=None, attachment=None, quote=None,
                     replace_mentions=True):
        """"""
        params = {**prepare_recipient(recipient), "message":text}
        if attachment is not None:
            if not isinstance(attachment, list):
                attachment = [attachment]
            attachment = [SendAttachment(item, self.local_data,
                                         self.signalcli_data) \
                          for item in attachment]
            params["attachments"] = [item.signalcli_filepath \
                                     for item in attachment]
        if quote is not None:
            params["quoteTimestamp"] = quote.timestamp
            params["quoteAuthor"] = quote.user.number
            params["quoteMessage"] = quote.text
            if len(quote.mentions) > 0:
                params["quoteMention"] = [mention.string() \
                                          for mention in quote.mentions]
        if replace_mentions is True and text is not None:
            params["mention"] = [f"{match.start(0)}:{len(match.group(0))}:" \
                                 "{match.group(1)}" \
                                 for match in \
                                 re.finditer(r"@(\+\d{10,20})", text)]
        response = self.rpc_call("send", params)
        if attachment is not None:
            map(lambda item: item.remove())
        return response

    def send_response(self, message, text, attachment=None, quote=True,
                      replace_mentions=True):
        """"""
        if not isinstance(message, DataMessage):
            raise SignalBotError("Responding is only works for DataMessage!")
        recipient = list(prepare_recipient(message).values())[0]
        if quote is True:
            quote_message = message
        else:
            quote_message = None
        return self.send_message(recipient, text, attachment, quote_message,
                                 replace_mentions)

    def send_sticker(self, recipient, pack_title, emoji):
        """"""
        for stickerpack in self.stickerpacks:
            if stickerpack.title == pack_title:
                sticker = stickerpack.get_id(emoji)
                break
        else:
            raise SignalBotError(f"No sticker for {emoji} found in " \
                                 "stickerpack {pack_title} or " \
                                 "even stickerpack not found!")
        params = {**prepare_recipient(recipient), "sticker":sticker}
        return self.rpc_call("send", params)

    def send_reaction(self, message, emoji, remove=False):
        """"""
        if not isinstance(message, DataMessage):
            raise SignalBotError("Reacting is only possible for DataMessage!")
        params = {**prepare_recipient(message), "emoji":emoji,
                  "targetAuthor":message.user.number,
                  "targetTimestamp":message.timestamp, "remove":remove}
        return self.rpc_call("sendReaction", params)

    def send_receipt(self, message, viewed=False):
        """"""
        params = {"recipient":message.user.number,
                  "targetTimestamp":message.timestamp}
        if viewed is True:
            params["type"] = "viewed"
        else:
            params["type"] = "read"
        return self.rpc_call("sendReceipt", params)

    def send_typing(self, recipient, stop=False, timeout=None):
        """"""
        params = prepare_recipient(recipient)
        if timeout is None:
            params["stop"] = stop
            return self.rpc_call("sendTyping", params)
        responses = []
        schedule = [*([10] * int(timeout // 10)), timeout % 10]
        for seconds in schedule:
            responses.append(self.rpc_call("sendTyping", params))
            time.sleep(seconds)
        params["stop"] = True
        responses.append(self.rpc_call("sendTyping", params))
        return responses

    def remote_delete(self, response):
        """"""
        params = {**prepare_recipient(response),
                  "targetTimestamp":response.timestamp}
        return self.rpc_call("remoteDelete", params)

    def join_group(self, uri):
        """"""
        params = {"uri":uri}
        return self.rpc_call("joinGroup", params)

    def list_contacts(self):
        """"""
        return self.rpc_call("listContacts")

    def list_groups(self):
        """"""
        return self.rpc_call("listGroups")

    def list_identities(self, number=None):
        """"""
        params = {"number":number}
        return self.rpc_call("listIdentities", params)

    def update_profile(self, first_name=None, last_name=None, about=None,
                       about_emoji=None, avatar=None, remove_avatar=False):
        """"""
        params = {"givenName":first_name, "familyName":last_name,
                  "about":about, "aboutEmoji":about_emoji,
                  "removeAvatar":remove_avatar}
        if avatar is not None and remove_avatar is False:
            avatar = SendAttachment(avatar, self.local_data,
                                    self.signalcli_data)
            params["avatar"] = avatar.signalcli_filepath
        response = self.rpc_call("updateProfile", params)
        if avatar is not None:
            avatar.remove()
        return response

    def update_contact(self, number, name=None, expiration_seconds=None):
        """"""
        params = {"recipient":number, "name":name,
                  "expiration":expiration_seconds}
        return self.rpc_call("updateContact", params)

    def remove_contact(self, number, forget=True):
        """"""
        params = {"recipient":number, "forget": forget}
        return self.rpc_call("removeContact", params)

    def trust(self, number, safety_number=None, all_keys=False):
        """"""
        params = {"recipient":number, "trustAllKnownKeys":all_keys,
                  "verifiedSafetyNumber":safety_number}
        return self.rpc_call("trust", params)

    def refresh_stickerpacks(self):
        """"""
        manifests = glob.glob(os.path.join(self.local_data,
                                           "stickers/*/manifest.json"))
        parsed = []
        for manifest_path in manifests:
            with open(manifest_path) as file:
                hook = lambda dct: PrettyNamespace(**dct)
                manifest = json.load(file,
                                     object_hook=hook)
                manifest.id = manifest_path.split("/")[-2]
                parsed.append(Stickerpack(manifest))
        self.stickerpacks = parsed

    def load_attachments(self, message):
        """"""
        for attachment in message.attachments:
            path = os.path.join(self.local_data, "attachments", attachment.id)
            with open(path) as file:
                attachment.content = file.read()
        return message.attachments



def prepare_recipient(recipient):
    """"""
    if isinstance(recipient, Response):
        try:
            result = recipient.result.results[0].groupId
            return {"groupId":result}
        except AttributeError:
            pass
        numbers = []
        for result in recipient.result.results:
            numbers.append(result.recipientAddress.number)
        return {"recipient":numbers}
    if isinstance(recipient, DataMessage):
        if recipient.group is not None:
            return {"groupId":recipient.group.id}
        return {"recipient":recipient.user.number}
    if isinstance(recipient, list):
        for item in recipient:
            if len(item[0]) > 20:
                raise SignalBotError("Only phone numbers allowed for list " \
                                     "of recipients!")
        return {"recipient":recipient}
    if len(recipient) < 20:
        return {"recipient":recipient}
    return {"groupId":recipient}
