#!/usr/bin/env python3
from pyrogram import ChatMember, Client

import user_bot_kit.groups
import user_bot_kit.users

app = Client("my_account")


def clean_deleted_account(chat_id: int):
    remove_member = user_bot_kit.retry(user_bot_kit.users.remove_member)
    members = user_bot_kit.users.get_users(app, chat_id)
    for member in members:
        member: ChatMember
        if not member.user.is_deleted:
            continue
        remove_member(app, chat_id, member)


def main():
    app.start()
    for chat in user_bot_kit.groups.get_super_groups(app):
        print("#%s (%s)" % (chat.title, chat.id))
        clean_deleted_account(chat.id)
    app.stop()


if __name__ == "__main__":
    main()
