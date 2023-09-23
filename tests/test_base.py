import pytest
from unittest.mock import patch, Mock, call

import random
from cmdpkg.base import BaseRunner, RunOutput, Command


@pytest.fixture(scope="module")
def output_factory(binary_io_factory):
    def factory():
        return RunOutput(binary_io_factory(), binary_io_factory(), random.randint(1, 256))

    return factory


class TestBaseRunner:
    setattr(BaseRunner, '__abstractmethods__', set())

    @patch.object(BaseRunner, 'run')
    def test_run_batch(self, run_mock: Mock, cmd_factory, output_factory):
        cmd1, command2 = cmd_factory(), Command(cmd_factory())
        output1, output2 = output_factory(), output_factory()
        run_mock.side_effect = [output1, output2]
        runner = BaseRunner()

        return_value = runner.run_batch(cmd1, command2)

        run_mock.assert_has_calls([call(cmd1), call(command2)])
        assert return_value == [output1, output2]

    @patch.object(BaseRunner, 'run')
    def test_run_pipe(self, run_mock: Mock, cmd_factory, output_factory, binary_io_factory):
        command1, command2 = Command(cmd_factory(), stdin=binary_io_factory()), Command(cmd_factory())
        output1, output2 = output_factory(), output_factory()
        run_mock.side_effect = [output1, output2]
        runner = BaseRunner()

        return_value = runner.run_pipe(command1, command2)

        run_mock.assert_has_calls([call(command1), call(command2)])
        assert command2.stdin == output1.stdout
        assert return_value == output2

    def test_run_pipe_raises_type_error(self, cmd_factory, binary_io_factory):
        cmd1, command2 = cmd_factory(), Command(cmd_factory())
        runner = BaseRunner()

        with pytest.raises(TypeError):
            runner.run_pipe(cmd1, command2)

    def test_run_pipe_raises_value_error(self, cmd_factory, binary_io_factory):
        cmd, command = cmd_factory(), Command(cmd_factory())
        command_with_stdin = Command(cmd_factory(), stdin=binary_io_factory())
        runner = BaseRunner()

        with pytest.raises(ValueError):
            runner.run_pipe(cmd)

        with pytest.raises(ValueError):
            runner.run_pipe(command, command_with_stdin)
