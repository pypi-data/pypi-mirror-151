from __future__ import annotations

from ..types import *

__all__ = [
    'Filter',
]


class Filter:

    def check(self, update: Update) -> bool:
        pass
