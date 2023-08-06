from __future__ import annotations

import logging
import os

import requests
from dotenv import load_dotenv

from .. import errors
from ..methods import *

BOT_TOKEN = 'BOT_TOKEN'
API_ENDPOINT = 'https://api.telegram.org/bot{token}/{method}'


class BotLayer0:

    def _validate_token(self):
        parts = self.token.split(':')

        if self.token.count(' ') == 0 and len(parts) == 2:
            if parts[0].isdigit() and parts[1].isascii():
                return True
        raise ValueError('Invalid token')

    def __init__(self, token: str = None):
        load_dotenv('.env')

        self.token = token or os.environ.get(BOT_TOKEN)

        if self.token is None:
            raise ValueError(f'You must set token or ${BOT_TOKEN}')

        self._validate_token()

        self.logger = logging.getLogger('bot')
        self.session = requests.Session()

    @property
    def id(self):
        return int(self.token.split(':')[0])

    def request(self, method: Method) -> dict | list | bool | str | int:
        url = API_ENDPOINT.format(token=self.token, method=method.__class__.__name__)
        resp = self.session.post(url, json=method.dict(exclude_none=True))
        result: dict = resp.json()

        if result['ok']:
            return result['result']
        else:
            raise errors.Error(result['error_code'], result['description'])
