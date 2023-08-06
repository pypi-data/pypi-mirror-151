from contextvars import ContextVar

from async_tg_bot.types import *
from .bot import Bot

__all__ = [
    'ctx',
]

BOT = ContextVar('bot')
MESSAGE = ContextVar('message')
USER = ContextVar('user')
CHAT = ContextVar('chat')
UPDATE = ContextVar('update')


class Context:

    def __init__(self):
        self._bot = BOT
        self._message = MESSAGE
        self._user = USER
        self._chat = CHAT
        self._update = UPDATE

    @property
    def message(self) -> Message:
        return self._message.get()

    @message.setter
    def message(self, value: Message):
        self._message.set(value)

    @property
    def user(self) -> User:
        return self._user.get()

    @user.setter
    def user(self, value: User):
        self._user.set(value)

    @property
    def chat(self) -> Chat:
        return self._chat.get()

    @chat.setter
    def chat(self, value: chat):
        self._chat.set(value)

    @property
    def bot(self) -> Bot:
        return self._bot.get()

    @bot.setter
    def bot(self, value: bot):
        self._bot.set(value)

    @property
    def update(self) -> Update:
        return self._update.get()

    @update.setter
    def update(self, value: update):
        self._update.set(value)


ctx = Context()
