import time
from datetime import datetime

from pyrogram.errors import FloodWait, BadRequest

from user_bot_kit.groups import get_super_groups
from user_bot_kit.users import remove_member, get_user, get_users

__all__ = [
    "get_super_groups",
    "get_user",
    "get_users",
    "remove_member",
    "retry",
]


def retry(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except BadRequest as err:
            print(repr(err))
            if err.ID == "PEER_ID_INVALID":
                return
            func(*args, **kwargs)
        except FloodWait as err:
            end_date = datetime \
                .fromtimestamp(time.time() + err.x) \
                .isoformat()
            print("Sleeping for %ds (%s)" % (err.x, end_date))
            time.sleep(err.x)
            func(*args, **kwargs)

    return wrapper
