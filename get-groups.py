#!/usr/bin/env python3
import time
from itertools import chain
from typing import Generator

from pyrogram import Chat, ChatMember, Client, Dialog
from pyrogram.errors import BadRequest, FloodWait

app = Client("my_account")


def get_groups() -> Generator[Chat, None, None]:
    for dialog in app.iter_dialogs():
        dialog: Dialog
        yield dialog.chat


def main():
    app.start()
    for chat in sorted(get_groups(), key=lambda chat: chat.id):
        print("#%14s | %-20s | %s" % (chat.type, chat.id, chat.title))
    app.stop()


if __name__ == "__main__":
    main()
