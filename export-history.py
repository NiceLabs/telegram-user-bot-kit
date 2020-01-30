#!/usr/bin/env python3
import csv
import sys
import time
from datetime import datetime, timedelta

from pyrogram import ChatMember, Client, Message
from pyrogram.api.functions.users import GetFullUser
from pyrogram.api.types import UserFull
from pyrogram.errors import BadRequest, FloodWait

app = Client("my_account")
enable_get_bio = True


def export_members(chat_id: int):
    fp = open("data/%s-members.csv" % chat_id, "w", encoding="utf-8-sig", newline="")
    writer = csv.DictWriter(fp, fieldnames=[
        "User ID",
        "Joined Date",
        "Status",
        "Photo",
        "First name",
        "Last name",
        "Username",
        "Bio",
    ])
    count = app.get_chat_members_count(chat_id=chat_id)
    for index, member in enumerate(app.iter_chat_members(chat_id=chat_id)):
        index: int
        member: ChatMember
        if index % 100 == 0 or index % round(count / 20) == 0:
            print("## {:>6d} / {:<6d} = {:.2%}".format(index, count, index / count))
        try:
            writer.writerow(get_user(member))
        except BadRequest as e:
            print("#%s #%s %s" % (chat_id, member.user.id, e.MESSAGE))
        except FloodWait as err:
            time.sleep(err.x + 0.5)
            writer.writerow(get_user(member))
        fp.flush()
    fp.close()


def get_user(member: ChatMember):
    joined_date = None
    if member.joined_date:
        joined_date = datetime \
            .fromtimestamp(member.joined_date) \
            .astimezone() \
            .isoformat()
    bio = None
    if enable_get_bio:
        fully: UserFull = app.send(GetFullUser(id=member.user.id))
        bio = fully.about
    return {
        "User ID": member.user.id,
        "Joined Date": joined_date,
        "Status": member.status,
        "Photo": None if member.user.photo else "Unset",
        "First name": member.user.first_name,
        "Last name": member.user.last_name,
        "Username": member.user.username,
        "Bio": bio,
    }


def export_history(chat_id: int):
    fp = open("data/%s-history.csv" % chat_id, "w", newline="")
    writer = csv.writer(fp)
    writer.writerow(["Date", "User ID"])
    count = app.get_history_count(chat_id=chat_id)
    for index, message in enumerate(app.iter_history(chat_id=chat_id)):
        message: Message
        if not message.from_user:
            continue
        if message.service or message.empty or message.media or message.via_bot:
            continue
        if index % 100 == 0 or index % round(count / 20) == 0:
            print("## {:>6d} / {:<6d} = {:.2%}".format(index, count, index / count))
        message_date = datetime.fromtimestamp(message.date)
        delta: timedelta = datetime.now() - message_date
        if delta.days >= 730:
            break
        send_date = message_date.astimezone().isoformat()
        writer.writerow([send_date, message.from_user.id])
    fp.close()


def main():
    chat_id = int(sys.argv[1])
    app.start()
    export_members(chat_id)
    export_history(chat_id)
    app.stop()


if __name__ == "__main__":
    main()
