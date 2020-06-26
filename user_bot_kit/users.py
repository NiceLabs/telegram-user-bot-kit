import time
from datetime import datetime
from itertools import chain

from pyrogram import Client, ChatMember
from pyrogram.api.functions.users import GetFullUser
from pyrogram.api.types import UserFull

from user_bot_kit import retry


def remove_member(app: Client, chat_id: int, member: ChatMember):
    user_id = member.user.id
    if member.status == "member":
        until_date = int(time.time() + 60)
        app.kick_chat_member(chat_id, user_id, until_date)
        print("#%s #%s Deleted" % (chat_id, user_id))
    elif member.status in ("kicked", "restricted"):
        app.unban_chat_member(chat_id, user_id)
        print("#%s #%s Unbanned" % (chat_id, user_id))


@retry
def get_user(app: Client, member: ChatMember, get_bio=False):
    joined_date = None
    if member.joined_date:
        joined_date = datetime \
            .fromtimestamp(member.joined_date) \
            .astimezone() \
            .isoformat()
    bio = None
    if get_bio:
        fully: UserFull = app.send(GetFullUser(id=member.user.id))
        bio = fully.about
    return {
        "User ID": str(member.user.id),
        "Joined Date": joined_date,
        "Status": member.status,
        "Photo": None if member.user.photo else "Unset",
        "First name": member.user.first_name,
        "Last name": member.user.last_name,
        "Username": member.user.username,
        "Bio": bio,
    }


def get_users(app: Client, chat_id: int):
    return chain(
        app.iter_chat_members(chat_id=chat_id, filter="kicked"),
        app.iter_chat_members(chat_id=chat_id, filter="restricted"),
        app.iter_chat_members(chat_id=chat_id),
    )
