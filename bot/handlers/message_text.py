"""Echoes only text messages; ignores stickers, photos and other content."""

from typing import Any

from bot.handlers.handler import Handler, HandlerStatus
from bot.messenger import Messenger


class MessageTextHandler(Handler):
    def can_handle(self, update: dict[str, Any]) -> bool:
        message = update.get("message")
        return isinstance(message, dict) and isinstance(message.get("text"), str)

    def handle(self, update: dict[str, Any], messenger: Messenger) -> HandlerStatus:
        message = update["message"]
        messenger.send_message(
            chat_id=message["chat"]["id"],
            text=message["text"],
        )
        return HandlerStatus.STOP
