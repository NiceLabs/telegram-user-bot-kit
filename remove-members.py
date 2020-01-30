#!/usr/bin/env python3
import csv
import sys
import time
from datetime import datetime
from itertools import chain

from pyrogram import Client, ChatMember
from pyrogram.errors import BadRequest, FloodWait

app = Client("my_account")


def get_user_ids(chat_id: int):
    members = chain(
        app.iter_chat_members(chat_id=chat_id),
        app.iter_chat_members(chat_id=chat_id, filter="kicked"),
        app.iter_chat_members(chat_id=chat_id, filter="restricted"),
    )
    for member in members:
        member: ChatMember
        yield member.user.id


def remove_user_ids(chat_id: int):
    with open("data/%s-removable.csv" % chat_id, "r") as fp:
        rows = csv.DictReader(fp, fieldnames=["User ID"])
        next(rows)
        for row in rows:
            yield int(row["User ID"])


def clean_deleted_account(chat_id: int, user_ids: set):
    for user_id in user_ids:
        try:
            until_date = int(time.time() + 60)
            app.kick_chat_member(chat_id, user_id, until_date)
            print("#%s #%s Deleted" % (chat_id, user_id))
        except BadRequest as err:
            print("#%s #%s %s" % (chat_id, user_id, err))
            if err.ID == "PEER_ID_INVALID":
                continue
            time.sleep(1)
            clean_deleted_account(chat_id, {user_id})
        except FloodWait as err:
            end_date = datetime \
                .fromtimestamp(time.time() + err.x) \
                .isoformat()
            print("#%s #%s Sleeping for %ds (%s)" % (chat_id, user_id, err.x, end_date))
            time.sleep(err.x)
            clean_deleted_account(chat_id, {user_id})


def main():
    chat_id = int(sys.argv[1])
    app.start()
    removable_user_ids = set(remove_user_ids(chat_id))
    current_user_ids = set(get_user_ids(chat_id))
    user_ids = removable_user_ids & current_user_ids
    print("remain count: %d" % len(user_ids))
    print("remain time: %.2f hours" % (len(user_ids) / 500))
    clean_deleted_account(chat_id, user_ids)
    app.stop()


if __name__ == "__main__":
    main()
