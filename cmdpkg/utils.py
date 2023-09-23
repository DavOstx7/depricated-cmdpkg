from typing import Iterable, Type


def filter_none_values(values: Iterable) -> filter:
    return filter(lambda value: value is not None, values)


def is_items_instance_of(args: Iterable, _type: Type) -> bool:
    for arg in args:
        if not isinstance(arg, _type):
            return False
    return True
