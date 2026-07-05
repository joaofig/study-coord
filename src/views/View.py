from typing import Callable, Awaitable

from tools.messenger import get_messenger
from viewmodels.ViewModel import ViewModel


class View:
    def __init__(self, vm: ViewModel):
        self.vm = vm
        self.vm.register(self._handle_notification)

    def _handle_notification(self, action: str, **kwargs):
        """Handle notifications from the ViewModel"""
        # This method can be overridden in subclasses to handle notifications
        pass

    @staticmethod
    async def broadcast(channel: str, message: str, **kwargs):
        """Broadcast a message to all registered handlers on the given channel"""
        messenger = get_messenger(channel)
        await messenger.send(message, **kwargs)

    @staticmethod
    def subscribe(channel: str, message: str, handler: Callable[..., None | Awaitable[None]]):
        """Subscribe a handler to a message on the given channel"""
        messenger = get_messenger(channel)
        messenger.subscribe(message, handler)
