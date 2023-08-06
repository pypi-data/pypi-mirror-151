from dataclasses import dataclass

__all__ = [
    'Code',
    'CONTINUE',
]


@dataclass
class Code:
    _code: int

    def __hash__(self):
        return self._code


CONTINUE = Code(0)
