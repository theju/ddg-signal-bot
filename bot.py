import dbus
import json
import urllib.parse

import requests

from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop


DBusGMainLoop(set_as_default=True)


PREFIX = '!bot'
DDG_API_URL = 'https://api.duckduckgo.com/'


def main(loop):
    sb = dbus.SessionBus()
    obj = sb.get_object("org.asamk.Signal", "/org/asamk/Signal")
    if not unwrap(obj.isRegistered()):
        print("Not Registered")
        return -1

    def message_received(timestamp, sender, groups, message, attachments):
        msg = message.strip()
        if not msg.startswith(f"{PREFIX} "):
            return None
        bang_resp = bang_api(msg)
        reply = f'{bang_resp["url"]}\n{bang_resp["text"]}'.strip()
        if not reply:
            reply = f"No results found for {msg}"
        if groups:
            recipient = groups
            obj.sendGroupMessage(
                dbus.String(reply),
                dbus.Array([], signature="s"),
                recipient
            )
        else:
            recipient = sender
            obj.sendMessage(
                dbus.String(reply),
                dbus.Array([], signature="s"),
                recipient
            )


    def sync_message_received(timestamp, sender, destination, groups, message, attachments):
        message_received(timestamp, destination, groups, message, attachments)


    def bang_api(message):
        msg = message.replace(f"{PREFIX} ", "").strip()
        is_bang = False
        if msg.startswith("!"):
            is_bang = True
        params = {
            "q": msg,
            "format": "json",
            "no_redirect": "1",
            "t": "ddg_sb",
        }
        if is_bang:
            params["no_redirect"] = "0"
        response = requests.get(f"{DDG_API_URL}?{urllib.parse.urlencode(params)}")
        if not response.ok:
            return None
        reply = {"url": "", "text": ""}
        if is_bang:
            reply["url"] = response.url
        else:
            jr = response.json()
            if jr["Redirect"] or jr["AbstractURL"]:
                reply["url"] = jr["Redirect"] or jr["AbstractURL"]
            if jr["AbstractText"] or jr["Definition"]:
                reply["text"] = jr["AbstractText"] or jr["Definition"]
        return reply

    obj.connect_to_signal("MessageReceived", message_received)
    obj.connect_to_signal("SyncMessageReceived", sync_message_received)

    loop.run()


def unwrap(dbus_obj):
    if type(dbus_obj) == dbus.Array:
        return [unwrap(ii) for ii in dbus_obj]
    elif type(dbus_obj) == dbus.ByteArray:
        return bytes(dbus_obj)
    elif type(dbus_obj) == dbus.Dictionary:
        return dict(dbus_obj)
    elif type(dbus_obj) == dbus.Struct:
        return tuple(dbus_obj)
    elif type(dbus_obj) == dbus.Signature:
        return str(dbus_obj)
    elif type(dbus_obj) == dbus.String:
        return str(dbus_obj)
    elif type(dbus_obj) == dbus.Byte:
        return chr(dbus_obj)
    elif type(dbus_obj) == dbus.Boolean:
        return bool(dbus_obj)
    elif type(dbus_obj) in [dbus.Int16, dbus.Int32, dbus.Int32]:
        return int(dbus_obj)
    return dbus_obj



if __name__ == '__main__':
    try:
        loop = GLib.MainLoop()
        main(loop)
    except KeyboardInterrupt:
        print("Quitting")
        loop.quit()
