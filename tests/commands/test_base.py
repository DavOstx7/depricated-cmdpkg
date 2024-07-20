import pytest
from unittest.mock import patch, Mock

from cmdpkg.commands.base import BaseCommand, Command


class TestBaseCommand:
    # No tests currently
    pass


class TestCommand:
    def test_equal_operator_overload_on_cmd(self):
        assert Command("ab") == "ab"
        assert Command(["a", "b"]) == ["a", "b"]

    def test_equal_operator_overload_on_command(self, binary_io_factory):
        binary_io = binary_io_factory()

        assert Command("ab") == Command("ab")
        assert Command(["a", "b"]) == Command(["a", "b"])
        assert Command("ab", timeout=1) == Command("ab", timeout=1)
        assert Command(["a", "b"], stdin=binary_io) == Command(["a", "b"], stdin=binary_io)

    @patch('cmdpkg.commands.utils.pipe_cmds')
    def test_pipe_operator_overload_on_cmd(self, pipe_cmds_mock: Mock, cmd_factory):
        cmd1, cmd2 = cmd_factory(), cmd_factory()
        command1 = Command(cmd1)

        return_value = command1 | cmd2

        pipe_cmds_mock.assert_called_once_with(cmd1, cmd2)
        assert return_value.cmd == pipe_cmds_mock.return_value
        assert return_value.timeout == command1.timeout
        assert return_value.stdin == command1.stdin

    @patch('cmdpkg.commands.utils.sum_timeouts')
    @patch('cmdpkg.commands.utils.pipe_cmds')
    def test_pipe_operator_overload_on_command(self, pipe_cmds_mock: Mock, sum_timeouts_mock: Mock, cmd_factory,
                                               timeout_factory):
        cmd1, cmd2 = cmd_factory(), cmd_factory()
        timeout1, timeout2 = timeout_factory(), timeout_factory()
        command1, command2 = Command(cmd1, timeout1), Command(cmd2, timeout2)

        return_value = command1 | command2

        pipe_cmds_mock.assert_called_once_with(cmd1, cmd2)
        sum_timeouts_mock.assert_called_once_with(timeout1, timeout2)
        assert return_value.cmd == pipe_cmds_mock.return_value
        assert return_value.timeout == sum_timeouts_mock.return_value
        assert return_value.stdin == command1.stdin

    def test_pipe_operator_overload_raises_value_error(self, binary_io_factory):
        binary_io1, binary_io2 = binary_io_factory(), binary_io_factory()

        with pytest.raises(ValueError):
            Command(["a", "b"]) | Command(["c", "d"], stdin=binary_io2)
