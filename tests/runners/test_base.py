import pytest
from unittest.mock import patch, Mock, call

import random
from cmdpkg.utils import set_class_abstract_methods
from cmdpkg.runners.base import IRunner, BaseRunner, BaseCommand, RunOutput


@pytest.fixture(scope="module")
def output_factory(binary_io_factory):
    def factory():
        return RunOutput(binary_io_factory(), binary_io_factory(), random.randint(1, 256))

    return factory


class TestIRunner:
    # No tests currently
    pass


class TestBaseRunner:
    set_class_abstract_methods(BaseRunner)

    @patch.object(BaseRunner, 'run')
    def test_run_batch(self, run_mock: Mock, cmd_factory, output_factory):
        cmd1, command2 = cmd_factory(), BaseCommand(cmd_factory())
        output1, output2 = output_factory(), output_factory()
        run_mock.side_effect = [output1, output2]
        runner = BaseRunner()

        return_value = runner.run_batch(cmd1, command2)

        run_mock.assert_has_calls([call(cmd1), call(command2)])
        assert return_value == [output1, output2]

    @patch('cmdpkg.runners.utils.validate_run_pipe_args')
    @patch.object(BaseRunner, 'run')
    def test_run_pipe(self, run_mock: Mock, validate_args: Mock, cmd_factory, output_factory, binary_io_factory):
        command1, command2 = BaseCommand(cmd_factory(), stdin=binary_io_factory()), BaseCommand(cmd_factory())
        output1, output2 = output_factory(), output_factory()
        run_mock.side_effect = [output1, output2]
        runner = BaseRunner()

        return_value = runner.run_pipe(command1, command2)

        validate_args.assert_called_once_with((command1, command2))
        run_mock.assert_has_calls([call(command1), call(command2)])
        assert command2.stdin == output1.stdout
        assert return_value == output2
