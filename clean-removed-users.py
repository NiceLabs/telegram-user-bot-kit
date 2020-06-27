#!/usr/bin/env python3
import sys

from itertools import chain
from pyrogram import Client

import user_bot_kit.users

app = Client("my_account")


def clean_removed_users(chat_id: int):
    remove_member = user_bot_kit.retry(user_bot_kit.users.remove_member)
    members = chain(
        app.iter_chat_members(chat_id=chat_id, filter="kicked"),
        app.iter_chat_members(chat_id=chat_id, filter="restricted")
    )
    for member in members:
        username = member.restricted_by.username
        if username and username.startswith("SCP_079"):
            continue
        remove_member(app, chat_id, member)


def main():
    app.start()
    for chat_id in sys.argv[1:]:
        clean_removed_users(int(chat_id))
    app.stop()


if __name__ == "__main__":
    main()
