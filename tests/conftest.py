# import random
# import string
# import pytest
# from unittest.mock import Mock
# from typing import BinaryIO, Callable
# from cmdpkg.connection import SSHConnectionDetails
# from cmdpkg.settings import ProcessRunnerSettings, ShellRunnerSettings, SSHRunnerSettings
# from cmdpkg.command import Command, CommandOutput
#
#
# def _random_string() -> str:
#     return ''.join(random.choices(
#         string.ascii_lowercase + string.ascii_uppercase + string.ascii_letters, k=random.randint(1, 10)
#     ))
#
#
# def _random_list() -> str:
#     return [_random_string() for _ in range(random.randint(1, 5))]
#
#
# def _random_number() -> int:
#     return random.randint(1, 100)
#
#
# def _fake_binary_io() -> BinaryIO:
#     return Mock(spec=BinaryIO)
#
#
# @pytest.fixture
# def fake_binary_io() -> BinaryIO:
#     return _fake_binary_io()
#
#
# @pytest.fixture
# def fake_ssh_connection_details() -> SSHConnectionDetails:
#     return SSHConnectionDetails(
#         hostname='1.1.1.1', username=_random_string(), password=_random_string(), port=_random_number()
#     )
#
#
# @pytest.fixture
# def fake_process_runner_settings() -> ProcessRunnerSettings:
#     return ProcessRunnerSettings(
#         ENV={_random_string(): _random_string()},
#         CWD=_random_string(),
#         STDIN=_fake_binary_io(),
#         STDOUT=_fake_binary_io(),
#         STDERR=_fake_binary_io(),
#     )
#
#
# @pytest.fixture
# def fake_shell_runner_settings() -> ShellRunnerSettings:
#     return ShellRunnerSettings(
#         ENV={_random_string(): _random_string()},
#         CWD=_random_string(),
#         STDIN=_fake_binary_io(),
#         STDOUT=_fake_binary_io(),
#         STDERR=_fake_binary_io(),
#     )
#
#
# @pytest.fixture
# def fake_ssh_runner_settings() -> SSHRunnerSettings:
#     return SSHRunnerSettings(
#         ENVIRONMENT={_random_string(), _random_string()}
#     )
#
#
# @pytest.fixture
# def fake_command_creator() -> Callable[[], Command]:
#     def creator():
#         primitive_command = random.choice([_random_list(), _random_string()])
#         timeout = random.choice([_random_number(), None])
#         stdin = random.choice([_fake_binary_io(), None])
#         return Command(primitive_command, timeout=timeout, stdin=stdin)
#
#     return creator
#
#
# @pytest.fixture
# def fake_command_creator() -> Callable[[], Command]:
#     def creator():
#         primitive_command = random.choice([_random_list(), _random_string()])
#         timeout = random.choice([_random_number(), None])
#         stdin = random.choice([_fake_binary_io(), None])
#         return Command(primitive_command, timeout=timeout, stdin=stdin)
#
#     return creator
#
#
# @pytest.fixture
# def fake_command_output_creator() -> Callable[[], CommandOutput]:
#     def creator():
#         return CommandOutput(stdout=_fake_binary_io(), stderr=_fake_binary_io(), exit_code=_random_number())
#
#     return creator


"""
import random
import string

import pytest
from unittest.mock import Mock

from cmdpkg.command import Command
from typing import BinaryIO


def _random_string() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def _random_float():
    return random.uniform(1, 100)


@pytest.fixture
def binary_io_factory():
    def factory():
        return Mock(spec=BinaryIO)

    return factory


@pytest.fixture
def command_factory(binary_io_factory):
    def factory():
        timeout = random.choice([_random_float(), None])
        stdin = random.choice([binary_io_factory(), None])
        return Command(_random_string(), timeout, stdin)

    return factory



"""