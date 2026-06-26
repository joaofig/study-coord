import asyncio
from abc import abstractmethod, ABC
from typing import Any

from src.tools.observability import Observable, ObserverHandler


class ViewModel(ABC):
    def __init__(self):
        super().__init__()
        self.observable = Observable()

    async def message(self, msg: str, **kwargs):
        result = self.handle_command(msg, **kwargs)
        if asyncio.iscoroutine(result):
            return await result
        return result

    @abstractmethod
    async def handle_command(self, msg: str, **kwargs):
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
