import pytest
from unittest.mock import patch, Mock

from cmdpkg.command import pipe_cmds, sum_timeouts
from cmdpkg.command import Command


def test_sum_timeouts():
    assert sum_timeouts(1, 2, 3) == 6
    assert sum_timeouts(1, None, 3) == 4
    assert sum_timeouts(None, None, None) is None


def test_pipe_cmds():
    assert pipe_cmds("ab", "cd") == "ab | cd"
    assert pipe_cmds(["a", "b"], ["c", "d"]) == ["a", "b", '|', "c", "d"]


def test_pipe_cmds_raises():
    with pytest.raises(TypeError):
        pipe_cmds("ab", ["c", "d"])
        pipe_cmds(["a", "b"], "cd")

    with pytest.raises(ValueError):
        pipe_cmds()
        pipe_cmds("ab")
        pipe_cmds(["a", "b"])


def test_equal_operator_overload_on_cmd():
    assert Command("ab") == "ab"
    assert Command(["a", "b"]) == ["a", "b"]


def test_equal_operator_overload_on_command(binary_io_factory):
    binary_io = binary_io_factory()

    assert Command("ab") == Command("ab")
    assert Command(["a", "b"]) == Command(["a", "b"])
    assert Command("ab", timeout=1) == Command("ab", timeout=1)
    assert Command(["a", "b"], stdin=binary_io) == Command(["a", "b"], stdin=binary_io)


@patch('cmdpkg.command.pipe_cmds')
def test_pipe_operator_overload_on_cmd(pipe_cmds_mock: Mock, cmd_factory):
    cmd1, cmd2 = cmd_factory(), cmd_factory()
    fake_command = Command(cmd1)

    fake_piped_command = fake_command | cmd2

    pipe_cmds_mock.assert_called_once_with(cmd1, cmd2)
    assert fake_piped_command.cmd == pipe_cmds_mock.return_value
    assert fake_piped_command.timeout == fake_command.timeout
    assert fake_piped_command.stdin == fake_command.stdin


@patch('cmdpkg.command.sum_timeouts')
@patch('cmdpkg.command.pipe_cmds')
def test_pipe_operator_overload_on_command(pipe_cmds_mock: Mock, sum_timeouts_mock: Mock, cmd_factory, timeout_factory):
    cmd1, cmd2 = cmd_factory(), cmd_factory()
    t1, t2 = timeout_factory(), timeout_factory()
    fake_command1, fake_command2 = Command(cmd1, t1), Command(cmd2, t2)

    fake_piped_command = fake_command1 | fake_command2

    pipe_cmds_mock.assert_called_once_with(cmd1, cmd2)
    sum_timeouts_mock.assert_called_once_with(t1, t2)
    assert fake_piped_command.cmd == pipe_cmds_mock.return_value
    assert fake_piped_command.timeout == sum_timeouts_mock.return_value
    assert fake_piped_command.stdin == fake_command1.stdin


def test_pipe_operator_overload_raises(binary_io_factory):
    binary_io1, binary_io2 = binary_io_factory(), binary_io_factory()

    with pytest.raises(ValueError):
        Command("ab", stdin=binary_io1) | Command("cd", stdin=binary_io2)
        Command(["a", "b"]) | Command(["c", "d"], stdin=binary_io2)
