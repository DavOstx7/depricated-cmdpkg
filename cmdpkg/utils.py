from typing import Tuple, Any, Optional


def filter_none_values(values: Tuple) -> filter:
    return filter(lambda value: value is not None, values)


def validate_minimum_length(args: Tuple[Any], minimum_length: int, message: Optional[str] = None):
    if len(args) < minimum_length:
        if message:
            raise ValueError(message)
        raise ValueError


def validate_same_type(args: Tuple[Any], message: Optional[str] = None):
    first_arg = args[0]
    for current_arg in args[1:]:
        if not type(first_arg) == type(current_arg):
            if message:
                raise TypeError(message)
            raise TypeError
