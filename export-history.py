#!/usr/bin/env python3
import csv
import time
from datetime import datetime, timedelta
from typing import Generator

from pyrogram import ChatMember, Client, Message
from pyrogram.api.functions.users import GetFullUser
from pyrogram.api.types import UserFull
from pyrogram.errors import BadRequest, FloodWait

app = Client("my_account")


def export_members(chat_id: int):
    fp = open("%s-members.csv" % chat_id, "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(fp)
    header = [
        "User ID",
        "Date",
        "Status",
        "Photo",
        "First name",
        "Last name",
        "Username",
        "Bio",
    ]
    writer.writerow(header)
    count = app.get_chat_members_count(chat_id=chat_id)
    for index, member in enumerate(app.iter_chat_members(chat_id=chat_id)):
        index: int
        member: ChatMember
        if index % 100 == 0 or index % round(count / 20) == 0:
            print("## {:>6d} / {:<6d} = {:.2%}".format(index, count, index / count))
        try:
            writer.writerow(get_full_user_row(member))
        except BadRequest as e:
            print("#%s #%s %s" % (chat_id, member.user.id, e.MESSAGE))
        except FloodWait as err:
            time.sleep(err.x)
            writer.writerow(get_full_user_row(member))
        fp.flush()
    fp.close()


def get_full_user_row(member: ChatMember):
    fully: UserFull = app.send(GetFullUser(id=app.resolve_peer(member.user.id)))
    joined_date = None
    if member.date:
        joined_date = datetime.fromtimestamp(member.date).astimezone().isoformat()
    return [
        fully.user.id,
        joined_date,
        member.status,
        None if fully.user.photo else "Unset",
        fully.user.first_name,
        fully.user.last_name,
        fully.user.username,
        fully.about,
    ]


def export_history(chat_id: int):
    fp = open("%s-history.csv" % chat_id, "w", newline="")
    writer = csv.writer(fp)
    writer.writerow(["Date", "User ID"])
    for message in app.iter_history(chat_id=chat_id):
        message: Message
        if message.service or message.empty or message.media or message.via_bot:
            continue
        message_date = datetime.fromtimestamp(message.date)
        delta: timedelta = datetime.now() - message_date
        if delta.days >= 730:
            break
        send_date = message_date.astimezone().isoformat()
        writer.writerow([send_date, message.from_user.id])
    fp.close()


def main():
    chat_id = int(input("Chat ID: "))
    app.start()
    export_members(chat_id)
    export_history(chat_id)
    app.stop()


if __name__ == "__main__":
    main()
