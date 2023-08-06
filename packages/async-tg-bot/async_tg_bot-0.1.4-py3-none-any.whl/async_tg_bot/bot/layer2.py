from .layer1 import BotLayer1
from .. import filters
from .. import utils
from ..handlers import Handler


class BotLayer2(BotLayer1):

    def on_update(self):
        _filters = []

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_any_message(self):
        _filters = [filters.IsAnyMessage()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_message(
            self,
            text: str | list[str] | filters.Text | list[filters.Text] = None,
            command: str | list[str] | filters.Command | list[filters.Command] = None,
    ):
        _filters = [filters.IsTextMessage()]

        for t in utils.listify(text):
            _filters.append(filters.Text.cast(t))

        for c in utils.listify(command):
            _filters.append(filters.Command.cast(c))

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _

    def on_photo(self):
        _filters = [filters.IsPhotoMessage()]

        def _(func):
            handler = Handler(func, _filters)
            self.handlers.add(handler)
            return func

        return _
