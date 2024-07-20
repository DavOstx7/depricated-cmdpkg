import pytest


def test_ssh_connection_details(fake_ssh_connection_details):
    assert fake_ssh_connection_details.connect_kwargs == {
        'hostname': fake_ssh_connection_details.hostname,
        'username': fake_ssh_connection_details.username,
        'password': fake_ssh_connection_details.password,
        'port': fake_ssh_connection_details.port
    }
