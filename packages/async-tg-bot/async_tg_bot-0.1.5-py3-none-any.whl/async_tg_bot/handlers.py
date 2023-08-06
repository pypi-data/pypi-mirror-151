from dataclasses import dataclass, field
from typing import Any

from . import codes, utils
from . import filters
from .methods import *
from .types import *


@dataclass
class Handler:
    func: Any
    _filters: list[filters.Filter] = field(default_factory=list)

    def notify(self, update: Update) -> set[codes.Code]:
        _codes = set()

        for f in self._filters:
            if not f.check(update):
                return {codes.CONTINUE}

        resp = self.func()

        for i in utils.listify(resp):
            if isinstance(i, Method):
                i.request()
            if isinstance(i, codes.Code):
                _codes.add(i)

        return _codes


@dataclass
class Handlers:
    _handlers: list[Handler] = field(default_factory=list)

    def add(self, handler: Handler):
        self._handlers.append(handler)

    def notify(self, update: Update):
        for handler in self._handlers:
            _codes = handler.notify(update)
            if codes.CONTINUE not in _codes:
                break
