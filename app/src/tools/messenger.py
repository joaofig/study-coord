from typing import Awaitable, Callable

from src.tools import singleton


class Messenger:
    def __init__(self):
        self.handlers = {}

    async def broadcast(self, message: str, **kwargs):
        if message in self.handlers.keys():
            for handler in self.handlers[message]:
                await handler(**kwargs)

    async def send(self, message: str, **kwargs):
        await self.broadcast(message, **kwargs)

    def subscribe(
        self, message: str, handler: Callable[..., None | Awaitable[None]]
    ) -> None:
        if message not in self.handlers:
            self.handlers[message] = [handler]
        else:
            self.handlers[message].append(handler)


@singleton
class MessengerHub:
    def __init__(self):
        self.hub = {}

    def __getitem__(self, message) -> Messenger:
        if message not in self.hub:
            self.hub[message] = Messenger()
        return self.hub[message]


def get_messenger(name: str) -> Messenger:
    return MessengerHub()[name]


async def send_message(messenger: str, message: str, **kwargs):
    msg = get_messenger(messenger)
    if msg:
        await msg.send(message, **kwargs)
