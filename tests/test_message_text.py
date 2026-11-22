import unittest
from unittest.mock import Mock

from bot.handlers.handler import HandlerStatus
from bot.handlers.message_text import MessageTextHandler


class TestMessageTextHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = MessageTextHandler()
        self.messenger = Mock()

    def test_echoes_same_text_to_same_chat(self) -> None:
        update = {"message": {"chat": {"id": 42}, "text": "Привет!"}}
        self.assertTrue(self.handler.can_handle(update))
        status = self.handler.handle(update, self.messenger)
        self.assertIs(status, HandlerStatus.STOP)
        self.messenger.send_message.assert_called_once_with(chat_id=42, text="Привет!")

    def test_ignores_photo(self) -> None:
        self.assertFalse(self.handler.can_handle({"message": {"photo": ["id"]}}))
        self.messenger.send_message.assert_not_called()

    def test_ignores_sticker(self) -> None:
        self.assertFalse(self.handler.can_handle({"message": {"sticker": "id"}}))
        self.messenger.send_message.assert_not_called()

    def test_empty_text_is_still_text(self) -> None:
        self.assertTrue(self.handler.can_handle({"message": {"text": ""}}))

    def test_ignores_non_message_update(self) -> None:
        self.assertFalse(self.handler.can_handle({"callback_query": {}}))
