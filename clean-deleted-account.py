#!/usr/bin/env python3
from itertools import chain

from pyrogram import ChatMember, Client

import user_bot_kit

app = Client("my_account")


def clean_deleted_account(chat_id: int):
    remove_member = user_bot_kit.retry(user_bot_kit.remove_member)
    members = chain(
        app.iter_chat_members(chat_id=chat_id, filter="kicked"),
        app.iter_chat_members(chat_id=chat_id, filter="restricted"),
        app.iter_chat_members(chat_id=chat_id),
    )
    for member in members:
        member: ChatMember
        if not member.user.is_deleted:
            continue
        remove_member(app, chat_id, member)


def main():
    app.start()
    for chat in user_bot_kit.get_super_groups(app):
        print("#%s (%s)" % (chat.title, chat.id))
        clean_deleted_account(chat.id)
    app.stop()


if __name__ == "__main__":
    main()
