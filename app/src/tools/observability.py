import asyncio
from collections.abc import Iterable
from typing import Callable, Mapping, Any, Coroutine, Set

from nicegui.observables import ObservableList, ObservableCollection

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
            result = handler(action, **kwargs)
            if asyncio.iscoroutine(result):
                await result


class GridList(ObservableList):
    def __init__(self,
                 data: list | None = None,
                 *,
                 on_change: Callable | None = None,
                 _parent: ObservableCollection | None = None,
                 ):
        super().__init__(data, on_change=on_change, _parent=_parent)

    def replace(self, new_items: Iterable):
        list.clear(self)
        self.extend(new_items)

    def delete(self, key: str, value: Any):
        removed = [r for r in self if r[key] != value]
        self.replace(removed)
