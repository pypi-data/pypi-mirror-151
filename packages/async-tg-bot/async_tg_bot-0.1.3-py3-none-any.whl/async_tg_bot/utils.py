from typing import TypeVar

T = TypeVar('T')


def listify(obj: T) -> T | list[T]:
    if obj is None:
        return []
    if isinstance(obj, list):
        return obj
    return [obj]
