from unittest.mock import patch, Mock, MagicMock

from cmdpkg.ssh import create_client, SSHRunner


@patch('paramiko.AutoAddPolicy', autospec=True)
@patch('paramiko.SSHClient', autospec=True)
def test_create_client_with_auto_add_policy(ssh_client_class_mock: MagicMock, auto_add_policy_class_mock: Mock):
    return_value = create_client(is_add_missing_host_keys=True)

    ssh_client_class_mock.assert_called_once_with()
    client_mock: Mock = ssh_client_class_mock()
    auto_add_policy_class_mock.assert_called_once_with()
    client_mock.set_missing_host_key_policy(auto_add_policy_class_mock())

    assert return_value == client_mock


@patch('paramiko.RejectPolicy', autospec=True)
@patch('paramiko.SSHClient', autospec=True)
def test_create_client_with_auto_add_policy(ssh_client_class_mock: MagicMock, reject_policy_class_mock: Mock):
    return_value = create_client(is_add_missing_host_keys=False)

    ssh_client_class_mock.assert_called_once_with()
    client_mock: Mock = ssh_client_class_mock()
    reject_policy_class_mock.assert_called_once_with()
    client_mock.set_missing_host_key_policy(reject_policy_class_mock())

    assert return_value == client_mock


def test_ssh_runner_connect():
    pass


def test_ssh_runner_run():
    pass


def test_ssh_runner_run_command():
    pass


def test_ssh_runner_run_primitive_command():
    pass
