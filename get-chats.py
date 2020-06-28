#!/usr/bin/env python3
from typing import Generator

from pyrogram import Chat, Client, Dialog

app = Client("bot")


# noinspection PyBroadException
def get_chats() -> Generator[Chat, None, None]:
    self_id = app.get_me().id
    for dialog in app.iter_dialogs():
        dialog: Dialog
        chat = dialog.chat
        status = None
        try:
            status = chat.get_member(self_id).status
        except:
            pass
        yield chat, status


def display_name(chat: Chat):
    if chat.title:
        return chat.title
    if chat.last_name:
        return chat.first_name + " " + chat.last_name
    return chat.first_name


def main():
    app.start()
    for chat, status in sorted(get_chats(), key=lambda _: _[1] or ""):
        row = "#%14s | %-20s | %-40s | %-13s | %s" % (
            chat.type,
            chat.id,
            chat.username or "",
            status or "",
            display_name(chat),
        )
        print(row)
    app.stop()


if __name__ == "__main__":
    main()
