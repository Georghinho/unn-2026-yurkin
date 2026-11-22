import json
import unittest
import urllib.parse
from unittest.mock import MagicMock, patch

from bot.telegram_messenger import TelegramMessenger


class TestTelegramMessenger(unittest.TestCase):
    @patch("bot.telegram_messenger.urllib.request.urlopen")
    def test_send_message_posts_original_text(self, urlopen: MagicMock) -> None:
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {"ok": True, "result": {"message_id": 7}}
        ).encode("utf-8")
        urlopen.return_value = response
        messenger = TelegramMessenger(token="123:TEST", base_url="https://example.org/")

        result = messenger.send_message(chat_id=14, text="Привет")

        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url, "https://example.org/bot123:TEST/sendMessage"
        )
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(
            urllib.parse.parse_qs(request.data.decode("utf-8")),
            {"chat_id": ["14"], "text": ["Привет"]},
        )
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 40)
        self.assertEqual(result, {"message_id": 7})

    @patch("bot.telegram_messenger.urllib.request.urlopen")
    def test_get_updates_encodes_allowed_updates(self, urlopen: MagicMock) -> None:
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {"ok": True, "result": [{"update_id": 17}]}
        ).encode("utf-8")
        urlopen.return_value = response
        messenger = TelegramMessenger(token="123:TEST", base_url="https://example.org")

        updates = messenger.get_updates(
            offset=10, timeout=30, allowed_updates=["message"]
        )

        request = urlopen.call_args.args[0]
        body = urllib.parse.parse_qs(request.data.decode("utf-8"))
        self.assertEqual(body["offset"], ["10"])
        self.assertEqual(body["timeout"], ["30"])
        self.assertEqual(body["allowed_updates"], ['["message"]'])
        self.assertEqual(updates, [{"update_id": 17}])

    @patch("bot.telegram_messenger.urllib.request.urlopen")
    def test_api_error_raises(self, urlopen: MagicMock) -> None:
        response = MagicMock()
        response.__enter__.return_value.read.return_value = (
            b'{"ok": false, "description": "bad request"}'
        )
        urlopen.return_value = response
        with self.assertRaisesRegex(RuntimeError, "bad request"):
            TelegramMessenger("123:TEST", "https://example.org").send_message(
                chat_id=14, text="hi"
            )
