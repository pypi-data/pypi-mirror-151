import time

from .layer0 import BotLayer0
from ..handler import Handler
from ..methods import *
from ..task import Task
from ..types import *


class BotLayer1(BotLayer0):
    def __init__(self, token: str = None):
        from ..context import ctx

        super().__init__(token)

        self.message_handlers: list[Handler] = []
        self.photo_handlers: list[Handler] = []

        self.tasks: list[Task] = []

        ctx.bot = self

    def task(self, delay: int = None):
        def deco(func):
            task = Task(func, delay)
            self.tasks.append(task)
            return func

        return deco

    @staticmethod
    def _notify_handlers(handlers: list[Handler], type_obj: Type):
        for handler in handlers:
            if handler.notify(type_obj):
                break

    def _process_update(self, update: Update):
        from ..context import ctx

        if update.message:
            message = update.message
            ctx.message = message
            ctx.user = message.from_user
            ctx.chat = message.chat

            if message.text:
                self._notify_handlers(self.message_handlers, message)
            if message.photo:
                self._notify_handlers(self.photo_handlers, message)

    def _process_updates(self, updates: list[Update]):
        for update in updates:
            self._process_update(update)

    def _run_tasks(self):
        for task in self.tasks:
            task.func()

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
        self._run_tasks()

        try:
            self._start_polling(poll_interval)
        except KeyboardInterrupt:
            self.logger.info('Stopping..')
