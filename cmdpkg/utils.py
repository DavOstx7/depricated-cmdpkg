from typing import Iterable, Type

ABSTRACT_METHODS_ATTRIBUTE = '__abstractmethods__'


def filter_none_values(values: Iterable) -> filter:
    return filter(lambda value: value is not None, values)


def is_items_instance_of(args: Iterable, _type: Type) -> bool:
    for arg in args:
        if not isinstance(arg, _type):
            return False
    return True


def set_class_abstract_methods(_class: Type):
    setattr(_class, ABSTRACT_METHODS_ATTRIBUTE, set())
