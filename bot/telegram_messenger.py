import json
import urllib.parse
import urllib.request
from typing import Any, cast

from bot.messenger import Messenger


REQUEST_TIMEOUT = 40


class TelegramMessenger(Messenger):
    def __init__(self, token: str, base_url: str) -> None:
        # Both values are provided by the caller, never hardcoded here.
        self._url = f"{base_url.rstrip('/')}/bot{token}"

    def _request_telegram_bot_api(self, method: str, **params: object) -> object:
        """POST to Telegram Bot API, return the 'result' field."""
        url = f"{self._url}/{method}"
        request = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(params).encode("utf-8"),
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            payload: dict[str, Any] = json.loads(response.read())
        if not payload["ok"]:
            raise RuntimeError(payload["description"])
        return cast(object, payload["result"])

    def get_updates(
        self,
        *,
        offset: int,
        timeout: int,
        allowed_updates: list[str],
    ) -> list[dict[str, Any]]:
       
        updates = cast(
            list[dict[str, Any]],
            self._request_telegram_bot_api(
                "getUpdates",
                offset=offset,
                timeout=timeout,
                allowed_updates=json.dumps(allowed_updates),
            ),
        )
        return updates

    def send_message(self, *, chat_id: int, text: str) -> dict[str, Any]:
        result = cast(
            dict[str, Any],
            self._request_telegram_bot_api(
                "sendMessage", chat_id=chat_id, text=text
            ),
        )
        return result
