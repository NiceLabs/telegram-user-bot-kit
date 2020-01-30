#!/usr/bin/env python3
import sys
from datetime import datetime, timedelta

from pyrogram import Client, Message

app = Client("my_account")


def remove_unable_message(message: Message):
    if not message.service:
        return
    deletable = message.left_chat_member or message.new_chat_members
    if not deletable:
        return
    message.delete()


def main():
    chat_id = int(sys.argv[1])
    app.start()
    for message in app.iter_history(chat_id=chat_id):
        delta: timedelta = datetime.now() - datetime.fromtimestamp(message.date)
        if delta.days >= 730:
            break
        remove_unable_message(message)
    app.stop()


if __name__ == "__main__":
    main()
