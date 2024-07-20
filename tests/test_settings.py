import pytest


def test_process_runner_settings(fake_process_runner_settings):
    assert fake_process_runner_settings.popen_kwargs == {
        'env': fake_process_runner_settings.ENV,
        'cwd': fake_process_runner_settings.CWD,
        'stdin': fake_process_runner_settings.STDIN,
        'stdout': fake_process_runner_settings.STDOUT,
        'stderr': fake_process_runner_settings.STDERR,
    }


def test_shell_runner_settings(fake_shell_runner_settings):
    assert fake_shell_runner_settings.popen_kwargs == {
        'env': fake_shell_runner_settings.ENV,
        'cwd': fake_shell_runner_settings.CWD,
        'stdin': fake_shell_runner_settings.STDIN,
        'stdout': fake_shell_runner_settings.STDOUT,
        'stderr': fake_shell_runner_settings.STDERR,
        'shell': True
    }


def test_ssh_runner_settings(fake_ssh_runner_settings):
    assert fake_ssh_runner_settings.exec_kwargs == {
        'environment': fake_ssh_runner_settings.ENVIRONMENT
    }
