#!/usr/bin/env python3
import time
from itertools import chain
from typing import Generator

from pyrogram import Chat, ChatMember, Client, Dialog
from pyrogram.errors import BadRequest, FloodWait

app = Client("my_account")


def get_supergroup() -> Generator[Chat, None, None]:
    self_id = app.get_me().id
    for dialog in app.iter_dialogs():
        dialog: Dialog
        chat = dialog.chat
        if chat.type != "supergroup":
            continue
        try:
            member = app.get_chat_member(chat.id, self_id)
            if not member.permissions:
                continue
            if not member.permissions.can_restrict_members:
                continue
        except Exception as e:
            print("#%s (%s): %s" % (chat.title, chat.id, repr(e)))
            continue
        yield chat


def remove_deleted_account(chat_id: int, member: ChatMember):
    if not member.user.is_deleted:
        return
    user_id = member.user.id
    if member.status == "member":
        app.kick_chat_member(chat_id, user_id)
        print("#%s #%s Deleted" % (chat_id, user_id))
    elif member.status in ("kicked", "restricted"):
        app.unban_chat_member(chat_id, user_id)
        print("#%s #%s Unban" % (chat_id, user_id))


def clean_deleted_account(chat_id: int):
    members = chain(
        app.iter_chat_members(chat_id=chat_id),
        app.iter_chat_members(chat_id=chat_id, filter="kicked"),
        app.iter_chat_members(chat_id=chat_id, filter="restricted"),
    )
    for member in members:
        member: ChatMember
        if not member.user.is_deleted:
            continue
        try:
            remove_deleted_account(chat_id, member)
        except BadRequest as e:
            print("#%s #%s %s" % (chat_id, member.user.id, e.MESSAGE))
            remove_deleted_account(chat_id, member)
        except FloodWait as e:
            print("#%s #%s %s" % (chat_id, member.user.id, e.MESSAGE))
            time.sleep(e.x)
            remove_deleted_account(chat_id, member)


def main():
    app.start()
    for chat in get_supergroup():
        print("#%s (%s)" % (chat.title, chat.id))
        clean_deleted_account(chat.id)
    app.stop()


if __name__ == "__main__":
    main()
