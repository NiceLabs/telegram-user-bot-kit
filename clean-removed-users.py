#!/usr/bin/env python3
import sys
import time
from datetime import datetime

from pyrogram import ChatMember, Client
from pyrogram.errors import BadRequest, FloodWait

app = Client("my_account")


# noinspection DuplicatedCode
def remove(chat_id: int, member: ChatMember):
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
        remove(chat_id, member)
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


def clean_removed_users(chat_id: int):
    for member in app.iter_chat_members(chat_id=chat_id, filter="kicked"):
        remove_member(chat_id, member)


def main():
    chat_id = int(sys.argv[1])
    app.start()
    clean_removed_users(chat_id)
    app.stop()


if __name__ == "__main__":
    main()
