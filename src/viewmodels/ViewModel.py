
import asyncio
from abc import abstractmethod, ABC
from typing import Any, Callable, Awaitable

from src.tools.observability import Observable, ObserverHandler
from tools.messenger import get_messenger


class ViewModel(ABC):
    def __init__(self):
        super().__init__()
        self.observable = Observable()

    @staticmethod
    async def broadcast(channel: str, message: str, **kwargs):
        """Broadcast a message to all registered handlers on the given channel"""
        messenger = get_messenger(channel)
        await messenger.broadcast(message, **kwargs)

    @staticmethod
    def subscribe(channel: str, message: str, handler: Callable[..., None | Awaitable[None]]):
        """Subscribe a handler to a message on the given channel"""
        messenger = get_messenger(channel)
        messenger.subscribe(message, handler)


    async def message(self, msg: str, **kwargs):
        """Use this method to send messages to the ViewModel. It will call the _on_message method and return the result."""
        result = self._on_message(msg, **kwargs)
        if asyncio.iscoroutine(result):
            return await result
        return result

    @abstractmethod
    async def _on_message(self, msg: str, **kwargs):
        """Base method for handling messages sent to the ViewModel"""
        return None

    def get(self, name: str) -> Any:
        """Get the value of a property from the ViewModel"""
        if not hasattr(self, name):
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")
        return getattr(self, name)

    def set(self, name: str, value: Any) -> None:
        """Set the value of a property on the ViewModel"""
        if not hasattr(self, name):
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")
        setattr(self, name, value)

    # Observable methods exposed through composition
    def register(self, handler: ObserverHandler):
        """Register a handler to receive messages from the ViewModel"""
        self.observable.register(handler)

    def unregister(self, handler: ObserverHandler) -> None:
        """Unregister a handler from receiving messages from the ViewModel"""
        self.observable.unregister(handler)

    async def notify(self, action: str, **kwargs) -> None:
        """Notify all registered handlers of a message from the ViewModel"""
        await self.observable.notify(action, **kwargs)
