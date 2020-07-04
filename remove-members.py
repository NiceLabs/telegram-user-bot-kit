#!/usr/bin/env python3
import csv
import sys
import time
from pyrogram import Client

import user_bot_kit.users

app = Client("bot")


def remove_user_ids(chat_id: int):
    with open("data/%s-removable.csv" % chat_id, "r") as fp:
        rows = csv.DictReader(fp, fieldnames=["User ID"])
        next(rows)
        for row in rows:
            yield int(row["User ID"])


def clean(chat_id: int):
    removable_user_ids = set(remove_user_ids(chat_id))
    current_user_ids = {member.user.id for member in app.iter_chat_members(chat_id=chat_id)}
    user_ids = removable_user_ids & current_user_ids

    print("remain count: %d" % len(user_ids))
    print("remain time: %.2f hours" % (len(user_ids) / 500))

    kick_chat_member = user_bot_kit.retry(app.kick_chat_member)
    for user_id in user_ids:
        until_date = int(time.time() + 60)
        kick_chat_member(chat_id, user_id, until_date)
        print("#%s #%s Deleted" % (chat_id, user_id))


def main():
    app.start()
    for chat_id in sys.argv[1:]:
        clean(int(chat_id))
    app.stop()


if __name__ == "__main__":
    main()
