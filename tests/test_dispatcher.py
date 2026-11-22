import unittest
from unittest.mock import Mock

from bot.dispatcher import Dispatcher
from bot.handlers.handler import HandlerStatus


class TestDispatcher(unittest.TestCase):
    def test_skips_handlers_that_cannot_handle(self) -> None:
        messenger = Mock()
        first = Mock()
        second = Mock()
        first.can_handle.return_value = False
        second.can_handle.return_value = True
        second.handle.return_value = HandlerStatus.STOP
        dispatcher = Dispatcher(messenger)
        dispatcher.add_handlers(first, second)
        update = {"message": {"text": "hi"}}

        dispatcher.dispatch(update)

        first.handle.assert_not_called()
        second.handle.assert_called_once_with(update, messenger)

    def test_stops_on_stop_status(self) -> None:
        first = Mock()
        second = Mock()
        first.can_handle.return_value = True
        first.handle.return_value = HandlerStatus.STOP
        dispatcher = Dispatcher(Mock())
        dispatcher.add_handlers(first, second)
        dispatcher.dispatch({"update_id": 1})
        second.can_handle.assert_not_called()

    def test_continues_on_continue_status(self) -> None:
        first = Mock()
        second = Mock()
        first.can_handle.return_value = True
        first.handle.return_value = HandlerStatus.CONTINUE
        second.can_handle.return_value = True
        second.handle.return_value = HandlerStatus.STOP
        dispatcher = Dispatcher(Mock())
        dispatcher.add_handlers(first, second)
        dispatcher.dispatch({"update_id": 1})
        second.handle.assert_called_once()
