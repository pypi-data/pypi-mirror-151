from __future__ import annotations

from dataclasses import dataclass

from .types import *

__all__ = [
    'Filter',
    'IsAnyMessage',
    'IsTextMessage',
    'IsPhotoMessage',
    'Command',
    'Text',
]


class Filter:

    def check(self, update: Update) -> bool:
        pass


class IsAnyMessage(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message)
        except AttributeError:
            return False


class IsTextMessage(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.text)
        except AttributeError:
            return False


class IsPhotoMessage(Filter):

    def check(self, update: Update):
        try:
            return bool(update.message.photo)
        except AttributeError:
            return False


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
