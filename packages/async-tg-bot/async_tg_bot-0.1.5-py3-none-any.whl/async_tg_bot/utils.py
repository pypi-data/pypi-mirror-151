from typing import TypeVar

T = TypeVar('T')


def listify(obj: T) -> T | list[T]:
    if obj is None:
        return []
    if isinstance(obj, list):
        return obj
    if isinstance(obj, tuple):
        return list(obj)

    return [obj]
