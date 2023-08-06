from .layer1 import BotLayer1
from .. import filters
from .. import utils
from ..handler import Handler


class BotLayer2(BotLayer1):

    def on_message(
            self,
            text: str = None,
            command: str | list[str] | filters.Command | list[filters.Command] = None,
    ):
        _filters = []
        texts = utils.listify(text)
        commands = utils.listify(command)

        for t in texts:
            if isinstance(t, str):
                t = filters.Text(t)
            _filters.append(t)

        for c in commands:
            if isinstance(c, str):
                c = filters.Command(c)
            _filters.append(c)

        def deco(func):
            handler = Handler(func, _filters)
            self.message_handlers.append(handler)
            return func

        return deco

    def on_photo(
            self,
            # caption: str | re.Pattern = None,
    ):
        def deco(func):
            handler = Handler(func, [])
            self.photo_handlers.append(handler)
            return func

        return deco

    # def on_any_message(self):
    #     pass
