from dataclasses import dataclass

from .types import *

__all__ = [
    'Filter',
    'Command',
]


class Filter:

    def check(self, typy_obj: Type) -> bool:
        return bool(typy_obj)


@dataclass
class Command(Filter):
    text: str

    def check(self, message: Message):
        if message.text == f'/{self.text}':
            return True


@dataclass
class Text(Filter):
    text: str

    def check(self, message: Message):
        if message.text == self.text:
            return True
