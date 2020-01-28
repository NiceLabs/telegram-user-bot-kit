#!/usr/bin/env python3
import time
from datetime import datetime, timedelta
from typing import Generator

from pyrogram import Client, Message
from pyrogram.errors import BadRequest, FloodWait

app = Client("my_account")


def remove_unable_message(message: Message):
    if not message.service:
        return
    deletable = message.left_chat_member or message.new_chat_members
    if not deletable:
        return
    message.delete()


def main():
    chat_id = int(input("Chat ID: "))
    app.start()
    for message in app.iter_history(chat_id=chat_id):
        delta: timedelta = datetime.now() - datetime.fromtimestamp(message.date)
        if delta.days >= 90:
            break
        remove_unable_message(message)
    app.stop()


if __name__ == "__main__":
    main()
