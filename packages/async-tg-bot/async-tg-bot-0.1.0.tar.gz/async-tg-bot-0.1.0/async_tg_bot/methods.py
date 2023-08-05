from pydantic import BaseModel

from .types import *

__all__ = [
    'SendMessage',
]


class Method(BaseModel):
    @property
    def _bot(self):
        from test import bot
        return bot

    def request(self) -> dict:
        return self._bot.request(self)


class SendMessage(Method):
    text: str
    chat_id: int = None

    def request(self) -> Message:
        result = super().request()
        return Message(**result)
