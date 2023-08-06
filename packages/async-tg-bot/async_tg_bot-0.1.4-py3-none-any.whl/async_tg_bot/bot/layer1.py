import time

from .layer0 import BotLayer0
from ..handlers import Handlers
from ..methods import *
from ..tasks import Task, Tasks
from ..types import *


class BotLayer1(BotLayer0):
    def __init__(self, token: str = None):
        from ..context import ctx

        super().__init__(token)

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

        if update.message:
            ctx.message = update.message
            ctx.user = update.message.from_user
            ctx.chat = update.message.chat

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
