import asyncio
from typing import Callable, Mapping, Any, Coroutine, Set

ObserverHandler = Callable[[str, Mapping[str, Any]], None] | Coroutine[Any, Any, None]


class Observable:
    def __init__(self, **kwargs):
        self._handlers: Set[ObserverHandler] = set()
        super().__init__(**kwargs)

    def register(self, handler: ObserverHandler):
        if handler not in self._handlers:
            self._handlers.add(handler)

    def unregister(self, handler: ObserverHandler) -> None:
        if handler in self._handlers:
            self._handlers.remove(handler)

    async def notify(self, action: str, **kwargs) -> None:
        for handler in self._handlers:
            result = handler(action, kwargs)
            if asyncio.iscoroutine(result):
                await result