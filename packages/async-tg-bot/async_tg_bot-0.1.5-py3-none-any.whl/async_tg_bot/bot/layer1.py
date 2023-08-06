import time

from .layer0 import BotLayer0
from ..handlers import Handlers
from ..methods import *
from ..tasks import Task, Tasks
from ..types import *


class BotLayer1(BotLayer0):

    def __init__(
            self,
            token: str = None,
            parse_mode: str = None,
            disable_web_page_preview: bool = None,
            disable_notification: bool = None,
            protect_content: bool = None,
            allow_sending_without_reply: bool = None,
    ):
        from ..context import ctx

        super().__init__(token)

        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.disable_notification = disable_notification
        self.protect_content = protect_content
        self.allow_sending_without_reply = allow_sending_without_reply

        self.handlers = Handlers()
        self.tasks = Tasks()

        ctx.bot = self

    def task(self, delay: int = 0):
        def _(func):
            task = Task(func, delay)
            self.tasks.add(task)
            return func

        return _

    def _process_update(self, update: Update):
        from ..context import ctx

        ctx.update = update

        ctx.message = update.message or update.edited_message or update.channel_post or update.edited_channel_post
        ctx.inline_query = update.inline_query
        ctx.chosen_inline_result = update.chosen_inline_result
        ctx.callback_query = update.callback_query
        ctx.shipping_query = update.shipping_query
        ctx.pre_checkout_query = update.pre_checkout_query
        ctx.poll = update.poll
        ctx.poll_answer = update.poll_answer
        ctx.chat_member = update.my_chat_member or update.chat_member
        ctx.chat_join_request = update.chat_join_request

        if ctx.message:
            ctx.user = ctx.message.from_user
            ctx.chat = ctx.message.chat

        if ctx.inline_query:
            ctx.user = ctx.inline_query.from_user

        if ctx.chosen_inline_result:
            ctx.user = ctx.chosen_inline_result.from_user

        if ctx.callback_query:
            ctx.user = ctx.callback_query.from_user
            if ctx.callback_query.message:
                ctx.chat = ctx.callback_query.message.chat

        if ctx.shipping_query:
            ctx.user = ctx.shipping_query.from_user

        if ctx.pre_checkout_query:
            ctx.user = ctx.pre_checkout_query.from_user

        if ctx.poll_answer:
            ctx.user = ctx.poll_answer.user

        if ctx.chat_member:
            ctx.chat = ctx.chat_member.chat
            ctx.user = ctx.chat_member.from_user

        if ctx.chat_join_request:
            ctx.chat = ctx.chat_join_request.chat
            ctx.user = ctx.chat_join_request.from_user

        try:
            self.handlers.notify(update)
        except Exception as e:
            self.logger.exception(e)

    def _process_updates(self, updates: list[Update]):
        for update in updates:
            self._process_update(update)

    def _start_polling(self, poll_interval):
        offset = None

        while True:
            updates = GetUpdates(offset=offset).request()

            if updates:
                self.logger.info(updates)
                self._process_updates(updates)
                offset = updates[-1].update_id + 1

            time.sleep(poll_interval)

    def run(self, poll_interval: float = 0.0):
        self.tasks.run()

        try:
            self._start_polling(poll_interval)
        except KeyboardInterrupt:
            self.logger.info('Stopping..')
