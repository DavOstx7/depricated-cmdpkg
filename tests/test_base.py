import pytest
from unittest.mock import patch, Mock, call

from cmdpkg._base import BaseRunner

BaseRunner.__abstractmethods__ = set()


@patch.object(BaseRunner, 'run')
def test_run_batch(run_mock: Mock, fake_command_creator, fake_command_output_creator):
    runner = BaseRunner()
    fake_cmd1, fake_cmd2 = fake_command_creator(), fake_command_creator()
    fake_output1, fake_output2 = fake_command_output_creator(), fake_command_output_creator()
    run_mock.side_effect = [fake_output1, fake_output2]

    return_value = runner.run_batch(fake_cmd1, fake_cmd2)

    run_mock.assert_has_calls([call(fake_cmd1), call(fake_cmd2)])
    assert return_value == [fake_output1, fake_output2]


@patch.object(BaseRunner, 'run')
def test_run_piped(run_mock: Mock, fake_command_creator, fake_command_output_creator):
    runner = BaseRunner()
    fake_cmd1, fake_cmd2 = fake_command_creator(), fake_command_creator()
    fake_output1, fake_output2 = fake_command_output_creator(), fake_command_output_creator()
    run_mock.side_effect = [fake_output1, fake_output2]

    return_value = runner.run_piped(fake_cmd1, fake_cmd2)

    run_mock.assert_has_calls([call(fake_cmd1), call(fake_cmd2)])
    assert fake_cmd2.stdin == fake_output1.stdout
    assert return_value == fake_output2
