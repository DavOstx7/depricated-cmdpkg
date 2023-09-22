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
        cmd, fake_command = cmd_factory(), Command(cmd_factory())
        fake_output1, fake_output2 = output_factory(), output_factory()
        run_mock.side_effect = [fake_output1, fake_output2]
        runner = BaseRunner()

        return_value = runner.run_batch(cmd, fake_command)

        run_mock.assert_has_calls([call(cmd), call(fake_command)])
        assert return_value == [fake_output1, fake_output2]

    @patch.object(BaseRunner, 'run')
    def test_run_pipe(self, run_mock: Mock, cmd_factory, output_factory, binary_io_factory):
        fake_command1, fake_command2 = Command(cmd_factory(), stdin=binary_io_factory()), Command(cmd_factory())
        fake_output1, fake_output2 = output_factory(), output_factory()
        run_mock.side_effect = [fake_output1, fake_output2]
        runner = BaseRunner()

        return_value = runner.run_pipe(fake_command1, fake_command2)

        run_mock.assert_has_calls([call(fake_command1), call(fake_command2)])
        assert fake_command2.stdin == fake_output1.stdout
        assert return_value == fake_output2

    def test_run_pipe_raises(self, cmd_factory, binary_io_factory):
        cmd, command = cmd_factory(), Command(cmd_factory())
        command_with_stdin = Command(cmd_factory(), stdin=binary_io_factory())
        runner = BaseRunner()

        with pytest.raises(ValueError):
            runner.run_pipe()
            runner.run_pipe(cmd)

        with pytest.raises(TypeError):
            runner.run_pipe(cmd, command)

        with pytest.raises(ValueError):
            runner.run_pipe(command, command_with_stdin)
