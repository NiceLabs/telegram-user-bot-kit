#!/usr/bin/env python3
import sys

from pyrogram import Client

import user_bot_kit

app = Client("my_account")


def clean_removed_users(chat_id: int):
    remove_member = user_bot_kit.retry(user_bot_kit.remove_member)
    for member in app.iter_chat_members(chat_id=chat_id, filter="kicked"):
        remove_member(app, chat_id, member)


def main():
    app.start()
    for chat_id in sys.argv[1:]:
        clean_removed_users(int(chat_id))
    app.stop()


if __name__ == "__main__":
    main()
