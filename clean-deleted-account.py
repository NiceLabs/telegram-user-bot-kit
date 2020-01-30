#!/usr/bin/env python3
import time
from datetime import datetime
from itertools import chain
from typing import Generator

from pyrogram import Chat, ChatMember, Client, Dialog
from pyrogram.errors import BadRequest, FloodWait

app = Client("my_account")


def get_super_groups() -> Generator[Chat, None, None]:
    self_id = app.get_me().id
    for dialog in app.iter_dialogs():
        dialog: Dialog
        chat = dialog.chat
        if chat.type != "supergroup":
            continue
        try:
            member = app.get_chat_member(chat.id, self_id)
            if not member.can_restrict_members:
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
        until_date = int(time.time() + 60)
        app.kick_chat_member(chat_id, user_id, until_date)
        print("#%s #%s Deleted" % (chat_id, user_id))
    elif member.status in ("kicked", "restricted"):
        app.unban_chat_member(chat_id, user_id)
        print("#%s #%s Unbanned" % (chat_id, user_id))


def remove_member(chat_id: int, member: ChatMember):
    user_id = member.user.id
    try:
        remove_deleted_account(chat_id, member)
    except BadRequest as err:
        print("#%s #%s %s" % (chat_id, user_id, err))
        remove_member(chat_id, member)
    except FloodWait as err:
        end_date = datetime \
            .fromtimestamp(time.time() + err.x) \
            .isoformat()
        print("#%s #%s Sleeping for %ds (%s)" % (chat_id, user_id, err.x, end_date))
        time.sleep(err.x)
        remove_member(chat_id, member)


def clean_deleted_account(chat_id: int):
    members = chain(
        app.iter_chat_members(chat_id=chat_id, filter="kicked"),
        app.iter_chat_members(chat_id=chat_id, filter="restricted"),
        app.iter_chat_members(chat_id=chat_id),
    )
    for member in members:
        member: ChatMember
        if not member.user.is_deleted:
            continue
        remove_member(chat_id, member)


def main():
    app.start()
    for chat in get_super_groups():
        print("#%s (%s)" % (chat.title, chat.id))
        clean_deleted_account(chat.id)
    app.stop()


if __name__ == "__main__":
    main()
