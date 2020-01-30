#!/usr/bin/env python3
import csv
import sys
from datetime import datetime

from pyrogram import Client, Message

app = Client("my_account")


def export_channel(chat_id: int):
    fp = open("data/%s-channel.csv" % chat_id, "w", newline="")
    writer = csv.writer(fp)
    writer.writerow(["Date", "Message"])
    for message in app.iter_history(chat_id=chat_id):
        message: Message
        if message.service or message.empty or message.media or message.via_bot:
            continue
        send_date = datetime.fromtimestamp(message.date) \
            .astimezone() \
            .isoformat()
        writer.writerow([send_date, message.text])
    fp.close()


def main():
    chat_id = int(sys.argv[1])
    app.start()
    export_channel(chat_id)
    app.stop()


if __name__ == "__main__":
    main()
