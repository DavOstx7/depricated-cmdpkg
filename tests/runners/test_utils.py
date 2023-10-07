import pytest

from cmdpkg.commands.base import BaseCommand
from cmdpkg.runners.utils import validate_run_pipe_args


def test_validate_run_pipe_args(cmd_factory):
    command1, command2 = BaseCommand(cmd_factory()), BaseCommand(cmd_factory())

    validate_run_pipe_args((command1, command2))


def test_run_pipe_raises_type_error(cmd_factory, binary_io_factory):
    cmd, command = cmd_factory(), BaseCommand(cmd_factory())

    with pytest.raises(TypeError):
        validate_run_pipe_args((cmd, command))


def test_run_pipe_raises_value_error(cmd_factory, binary_io_factory):
    cmd = cmd_factory()
    command, command_with_stdin = BaseCommand(cmd_factory()), BaseCommand(cmd_factory(), stdin=binary_io_factory())

    with pytest.raises(ValueError):
        validate_run_pipe_args((cmd,))

    with pytest.raises(ValueError):
        validate_run_pipe_args((command, command_with_stdin))
