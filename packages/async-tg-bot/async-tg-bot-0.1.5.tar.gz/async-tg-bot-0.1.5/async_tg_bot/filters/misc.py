from __future__ import annotations

from dataclasses import dataclass

from .filter import Filter
from ..types import *


@dataclass
class Command(Filter):
    text: str

    def check(self, update: Update):
        message = update.message

        if message.text == f'/{self.text}':
            return True

    @classmethod
    def cast(cls, command: str | Command) -> Command:
        if isinstance(command, str):
            return Command(command)
        return command


@dataclass
class Text(Filter):
    text: str

    def check(self, update: Update):
        message = update.message

        if message.text == self.text:
            return True

    @classmethod
    def cast(cls, text: str | Text) -> Text:
        if isinstance(text, str):
            return Text(text)
        return text


class IsCallbackQuery(Filter):

    def check(self, update: Update):
        try:
            return bool(update.callback_query)
        except AttributeError:
            return False


class IsAnyMessage(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message)
        except AttributeError:
            return False
