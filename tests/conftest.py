import random
import string

import pytest
from unittest.mock import Mock

from typing import BinaryIO


def _random_str():
    return "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))


def _random_str_list():
    return [_random_str() for _ in range(random.randint(1, 3))]


@pytest.fixture(scope="session")
def binary_io_factory():
    def factory():
        return Mock(spec=BinaryIO)

    return factory


@pytest.fixture(scope="session")
def timeout_factory():
    def factory():
        return random.uniform(1, 100)

    return factory


@pytest.fixture(scope="session")
def cmd_factory():
    def factory():
        return random.choice([_random_str(), _random_str_list()])

    return factory
