#!/usr/bin/env python3
from typing import Generator

from pyrogram import Chat, Client, Dialog

app = Client("my_account")


def get_chats() -> Generator[Chat, None, None]:
    for dialog in app.iter_dialogs():
        dialog: Dialog
        yield dialog.chat


def main():
    app.start()
    for chat in sorted(get_chats(), key=lambda chat: chat.id):
        print("#%14s | %-20s | %s" % (chat.type, chat.id, chat.title))
    app.stop()


if __name__ == "__main__":
    main()
