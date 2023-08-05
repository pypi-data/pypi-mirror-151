import logging
import os
from dataclasses import dataclass
from pydantic import BaseModel
import requests

from .types import *
from .methods import *

BOT_TOKEN = 'BOT_TOKEN'
API_ENDPOINT = 'https://api.telegram.org/bot{token}/{method}'


@dataclass
class Command:
    text: str


class Handler:
    def __init__(self, func, _filter):
        self.func = func
        self.filter = _filter


class Task:
    def __init__(self, func, delay: int = None):
        self.func = func
        self.delay = delay


@dataclass
class ApiError(Exception):
    error_code: int
    description: str


class BaseBot:

    def _validate_token(self):
        parts = self.token.split(':')

        if self.token.count(' ') == 0 and len(parts) == 2:
            if parts[0].isdigit() and parts[1].isascii():
                return True
        raise ValueError('Invalid token')

    def __init__(self, token: str = None):
        self.token = token or os.environ.get(BOT_TOKEN)

        if self.token is None:
            raise ValueError(f'You must set token or ${BOT_TOKEN}')

        self._validate_token()

        self.logger = logging.getLogger('bot')
        self.session = requests.Session()

    @property
    def id(self):
        return int(self.token.split(':')[0])

    def request(self, method: BaseModel) -> dict:
        url = API_ENDPOINT.format(token=self.token, method=method.__class__.__name__)
        resp = self.session.get(url, params=method.dict())
        result: dict = resp.json()

        if result['ok']:
            return result['result']
        else:
            raise ApiError(result['error_code'], result['description'])


class Bot(BaseBot):
    def __init__(self, token: str = None):
        super().__init__(token)

        self.message_handlers: list[Handler] = []

        self.tasks: list[Task] = []

    def on_message(self, command: str | list[str] | Command | list[Command] = None):
        def deco(func):
            handler = Handler(func, {'command': command})
            self.message_handlers.append(handler)
            return func

        return deco

    def task(self, delay: int = None):
        def deco(func):
            task = Task(func, delay)
            self.tasks.append(task)
            return func

        return deco

    def run(self):
        for task in self.tasks:
            task.func()

    # def get_me(self):
    #     result = self._request(method='getMe')
    #     return User(**result)
    #
    # def get_updates(self):
    #     result = self._request(method='getUpdates')
    #     return Update(**result[1])
