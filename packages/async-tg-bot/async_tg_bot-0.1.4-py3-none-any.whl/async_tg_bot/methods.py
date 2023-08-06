from pydantic import BaseModel

from .types import *

__all__ = [
    'Method',
    'SendMessage',
    'GetUpdates',
    'GetMe',
]


class Method(BaseModel):

    def request(self) -> dict:
        from .context import ctx

        return ctx.bot.request(self)


class SendMessage(Method):
    text: str
    chat_id: int = None

    # reply_markup: ReplyKeyboardMarkup | ReplyKeyboardRemove | InlineKeyboardMarkup = None

    def request(self) -> Message:
        from .context import ctx

        self.chat_id = self.chat_id or ctx.chat.id
        result = super().request()
        return Message(**result)


class GetUpdates(Method):
    offset: int = None
    limit: int = None
    timeout: int = None
    allowed_updates: list[str] = None

    def request(self) -> list[Update]:
        result = super().request()
        return [Update(**i) for i in result]


class GetMe(Method):

    def request(self) -> User:
        result = super().request()
        return User(**result)
