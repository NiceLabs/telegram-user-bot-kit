from pyrogram import Message


def is_bot_command(message: Message):
    if message.entities:
        return any(
            entity.type == "bot_command" and entity.offset == 0
            for entity in message.entities
        )
    return False
