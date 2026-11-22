import unittest
from unittest.mock import Mock, patch

from bot.long_polling import poll_once, start_long_polling


class TestLongPolling(unittest.TestCase):
    def test_receives_only_messages_and_updates_offset(self) -> None:
        messenger = Mock()
        dispatcher = Mock()
        messenger.get_updates.return_value = [
            {"update_id": 10, "message": {"text": "Первое"}},
            {"update_id": 13, "message": {"text": "Второе"}},
        ]

        next_offset = poll_once(dispatcher, messenger, offset=8)

        self.assertEqual(next_offset, 14)
        messenger.get_updates.assert_called_once_with(
            offset=8, timeout=30, allowed_updates=["message"]
        )
        self.assertEqual(dispatcher.dispatch.call_count, 2)

    def test_empty_batch_preserves_offset(self) -> None:
        messenger = Mock()
        messenger.get_updates.return_value = []
        self.assertEqual(poll_once(Mock(), messenger, offset=11), 11)

    @patch("bot.long_polling.logger.exception")
    @patch("bot.long_polling.time.sleep", side_effect=KeyboardInterrupt)
    def test_retries_after_failure(self, sleep: Mock, log_exception: Mock) -> None:
        messenger = Mock()
        messenger.get_updates.side_effect = ConnectionError("offline")
        with self.assertRaises(KeyboardInterrupt):
            start_long_polling(Mock(), messenger)
        sleep.assert_called_once_with(5)
        log_exception.assert_called_once()
