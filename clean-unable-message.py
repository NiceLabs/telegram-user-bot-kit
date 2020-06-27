#!/usr/bin/env python3
import sys
from datetime import datetime, timedelta
from typing import List

from pyrogram import Client, MessageEntity

app = Client("my_account")


def is_bot_command(entities: List[MessageEntity]):
    if not entities:
        return False
    return any(entity.type == "bot_command" for entity in entities)


def remove_unable_message(chat_id: int):
    for message in app.iter_history(chat_id=chat_id):
        delta: timedelta = datetime.now() - datetime.fromtimestamp(message.date)
        if delta.days >= 730:
            break
        if is_bot_command(message.entities):
            message.delete()
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
