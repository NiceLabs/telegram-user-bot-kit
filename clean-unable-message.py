#!/usr/bin/env python3
import sys
from datetime import datetime, timedelta

from pyrogram import Client

app = Client("my_account")


def remove_unable_message(chat_id: int):
    for message in app.iter_history(chat_id=chat_id):
        delta: timedelta = datetime.now() - datetime.fromtimestamp(message.date)
        if delta.days >= 730:
            break
        if not message.service:
            continue
        if message.left_chat_member or message.new_chat_members:
            message.delete()


def main():
    app.start()
    for chat_id in sys.argv[1:]:
        remove_unable_message(int(chat_id))
    app.stop()


if __name__ == "__main__":
    main()
