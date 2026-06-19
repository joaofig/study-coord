from abc import abstractmethod, ABC
from typing import Any

from tools.observability import Observable, ObserverHandler


class ViewModel(ABC):
    def __init__(self):
        super().__init__()
        self.observable = Observable()

    @abstractmethod
    async def async_message(self, msg: str, data: Any = None):
        """Base method for handling asynchronous messages sent to the ViewModel"""
        pass

    @abstractmethod
    def message(self, msg: str, data: Any = None):
        """Base method for handling messages sent to the ViewModel"""
        pass

    def register(self, handler: ObserverHandler):
        """Register a handler to receive messages from the ViewModel"""
        self.observable.register(handler)

    def unregister(self, handler: ObserverHandler) -> None:
        """Unregister a handler from receiving messages from the ViewModel"""
        self.observable.unregister(handler)

    def notify(self, action: str, **kwargs) -> None:
        """Notify all registered handlers of a message from the ViewModel"""
        self.observable.notify(action, **kwargs)

    async def async_notify(self, action: str, **kwargs) -> None:
        """Notify all registered handlers of a message from the ViewModel"""
        await self.observable.notify(action, **kwargs)
