#!/usr/bin/env python3
import csv
import sys
from datetime import datetime, timedelta

from pyrogram import ChatMember, Client, Message

from user_bot_kit import retry
from user_bot_kit.message import is_bot_command
from user_bot_kit.users import get_user

app = Client("bot")


def export_members(chat_id: int):
    count = app.get_chat_members_count(chat_id=chat_id)
    fetch = retry(get_user)
    for index, member in enumerate(app.iter_chat_members(chat_id=chat_id)):
        member: ChatMember
        if member.user.is_deleted:
            continue
        if index % 100 == 0 or index % round(count / 20) == 0:
            print("# {:>6d} / {:<6d} = {:.2%}".format(index, count, index / count))
        yield fetch(app, member, get_bio=False)


def export_history(chat_id: int):
    count = app.get_history_count(chat_id=chat_id)
    for index, message in enumerate(app.iter_history(chat_id=chat_id)):
        message: Message
        skippable = (
                is_bot_command(message)
                or not message.from_user
                or message.forward_from
                or message.empty
                or message.service
                or message.media
                or message.via_bot
        )
        if skippable:
            continue
        if index % 100 == 0 or index % round(count / 20) == 0:
            print("# {:>6d} / {:<6d} = {:.2%}".format(index, count, index / count))
        message_date = datetime.fromtimestamp(message.date)
        delta: timedelta = datetime.now() - message_date
        if delta.days >= 730:
            break
        send_date = message_date.astimezone().isoformat()
        yield {
            "Date": send_date,
            "User ID": str(message.from_user.id)
        }


def main():
    chat_id = int(sys.argv[1])
    app.start()
    with open("data/%s-members.csv" % chat_id, "w", encoding="utf-8-sig", newline="") as fp:
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
        writer.writeheader()
        writer.writerows(export_members(chat_id))
    with open("data/%s-history.csv" % chat_id, "w", encoding="utf-8-sig", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=[
            "Date",
            "User ID"
        ])
        writer.writeheader()
        writer.writerows(export_history(chat_id))
    app.stop()


if __name__ == "__main__":
    main()
