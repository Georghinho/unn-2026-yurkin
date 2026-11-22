from abc import ABC, abstractmethod
from typing import Any


class Messenger(ABC):
    @abstractmethod
    def get_updates(
        self,
        *,
        offset: int,
        timeout: int,
        allowed_updates: list[str],
    ) -> list[dict[str, Any]]:
        """Receive messenger events."""

    @abstractmethod
    def send_message(self, *, chat_id: int, text: str) -> dict[str, Any]:
        """Send a text message to a chat."""
