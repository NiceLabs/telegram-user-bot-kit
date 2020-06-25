from typing import Generator

from pyrogram import Client, Chat, Dialog


def get_super_groups(app: Client) -> Generator[Chat, None, None]:
    self_id = app.get_me().id
    for dialog in app.iter_dialogs():
        dialog: Dialog
        chat = dialog.chat
        if chat.type != "supergroup":
            continue
        try:
            member = app.get_chat_member(chat.id, self_id)
            if not member.can_restrict_members:
                continue
        except Exception as e:
            print("#%s (%s): %s" % (chat.title, chat.id, repr(e)))
            continue
        yield chat
