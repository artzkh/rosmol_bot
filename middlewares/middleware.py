from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class MessageMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        print(1)


class EventMiddleware(BaseMiddleware[dict]):
    async def pre(self):
        print(2)
