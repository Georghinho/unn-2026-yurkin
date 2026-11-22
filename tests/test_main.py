import os
import unittest
from unittest.mock import Mock, patch

from bot.__main__ import main


class TestMain(unittest.TestCase):
    @patch("bot.__main__.logger.info")
    @patch("bot.__main__.start_long_polling", side_effect=KeyboardInterrupt)
    @patch("bot.__main__.TelegramMessenger")
    def test_reads_exact_required_environment_variables(
        self, telegram_messenger: Mock, polling: Mock, log_info: Mock
    ) -> None:
        with patch.dict(
            os.environ,
            {
                "TELEGRAM_TOKEN": "123:TEST",
                "TELEGRAM_BASE_URL": "https://example.org",
            },
            clear=True,
        ):
            main()

        telegram_messenger.assert_called_once_with(
            token="123:TEST", base_url="https://example.org"
        )
        polling.assert_called_once()
        self.assertEqual(log_info.call_count, 2)
