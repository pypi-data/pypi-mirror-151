from . import filters
from .methods import *
from .types import Type


class Handler:
    def __init__(self, func, _filters: list[filters.Filter]):
        self.func = func
        self.filters = _filters

    def notify(self, type_obj: Type) -> bool:
        for f in self.filters:
            if not f.check(type_obj):
                return False

        result = self.func()
        if isinstance(result, Method):
            result.request()

        return True
