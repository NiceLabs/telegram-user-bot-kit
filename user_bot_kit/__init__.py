import time
from datetime import datetime

from pyrogram.errors import FloodWait, BadRequest


def retry(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except BadRequest as err:
            if err.ID == "PEER_ID_INVALID":
                raise
            print(repr(err))
            wrapper(*args, **kwargs)
        except FloodWait as err:
            end_date = datetime \
                .fromtimestamp(time.time() + err.x) \
                .isoformat()
            print("Sleeping for %ds (%s)" % (err.x, end_date))
            time.sleep(err.x)
            wrapper(*args, **kwargs)

    return wrapper
