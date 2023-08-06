from contextvars import ContextVar

from async_tg_bot.types import *
from .bot import Bot

__all__ = [
    'ctx',
]

BOT = ContextVar('bot')
PARSE_MODE = ContextVar('parse_mode')
DISABLE_WEB_PAGE_PREVIEW = ContextVar('d')

UPDATE = ContextVar('update')

MESSAGE = ContextVar('message')
INLINE_QUERY = ContextVar('inline_query')
CHOSEN_INLINE_RESULT = ContextVar('chosen_inline_result')
CALLBACK_QUERY = ContextVar('callback_query')
SHIPPING_QUERY = ContextVar('shipping_query')
PRE_CHECKOUT_QUERY = ContextVar('pre_checkout_query')
POLL = ContextVar('poll')
POLL_ANSWER = ContextVar('poll_answer')
CHAT_MEMBER = ContextVar('chat_member')
CHAT_JOIN_REQUEST = ContextVar('chat_join_request')

CHAT = ContextVar('chat')
USER = ContextVar('user')


class Context:

    @property
    def bot(self) -> Bot:
        return BOT.get(None)

    @bot.setter
    def bot(self, value: Bot):
        BOT.set(value)

    # ===

    @property
    def update(self) -> Update:
        return UPDATE.get(None)

    @update.setter
    def update(self, value: Update):
        UPDATE.set(value)

    # ===

    @property
    def message(self) -> Message:
        return MESSAGE.get(None)

    @message.setter
    def message(self, value: Message):
        MESSAGE.set(value)

    @property
    def inline_query(self) -> InlineQuery:
        return INLINE_QUERY.get(None)

    @inline_query.setter
    def inline_query(self, value: InlineQuery):
        INLINE_QUERY.set(value)

    @property
    def chosen_inline_result(self) -> ChosenInlineResult:
        return CHOSEN_INLINE_RESULT.get(None)

    @chosen_inline_result.setter
    def chosen_inline_result(self, value: ChosenInlineResult):
        CHOSEN_INLINE_RESULT.set(value)

    @property
    def callback_query(self) -> CallbackQuery:
        return CALLBACK_QUERY.get(None)

    @callback_query.setter
    def callback_query(self, value: CallbackQuery):
        CALLBACK_QUERY.set(value)

    @property
    def shipping_query(self) -> ShippingQuery:
        return SHIPPING_QUERY.get(None)

    @shipping_query.setter
    def shipping_query(self, value: ShippingQuery):
        SHIPPING_QUERY.set(value)

    @property
    def pre_checkout_query(self) -> PreCheckoutQuery:
        return PRE_CHECKOUT_QUERY.get(None)

    @pre_checkout_query.setter
    def pre_checkout_query(self, value: PreCheckoutQuery):
        PRE_CHECKOUT_QUERY.set(value)

    @property
    def poll(self) -> Poll:
        return POLL.get(None)

    @poll.setter
    def poll(self, value: Poll):
        POLL.set(value)

    @property
    def poll_answer(self) -> PollAnswer:
        return POLL_ANSWER.get(None)

    @poll_answer.setter
    def poll_answer(self, value: PollAnswer):
        POLL_ANSWER.set(value)

    @property
    def chat_member(self) -> ChatMemberUpdated:
        return CHAT_MEMBER.get(None)

    @chat_member.setter
    def chat_member(self, value: ChatMemberUpdated):
        CHAT_MEMBER.set(value)

    @property
    def chat_join_request(self) -> ChatJoinRequest:
        return CHAT_JOIN_REQUEST.get(None)

    @chat_join_request.setter
    def chat_join_request(self, value: ChatJoinRequest):
        CHAT_JOIN_REQUEST.set(value)

    #  ===

    @property
    def chat(self) -> Chat:
        return CHAT.get(None)

    @chat.setter
    def chat(self, value: Chat):
        CHAT.set(value)

    @property
    def user(self) -> User:
        return USER.get(None)

    @user.setter
    def user(self, value: User):
        USER.set(value)


ctx = Context()
