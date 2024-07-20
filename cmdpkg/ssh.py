import paramiko
from typing import Union, Optional
from cmdpkg._typing import EnvironmentT, KwargsT, PrimitiveCommandT
from cmdpkg._base import BaseRunner, Command, RunOutput
from cmdpkg.models import DataStreamer

DEFAULT_BUFFERING = -1
NO_BUFFERING = 0
LINE_BUFFERING = 1


class SSHConnectionDetails:
    def __init__(self, hostname: str, username: Optional[str] = None, password: Optional[str] = None, port: int = 22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    @property
    def connect_kwargs(self) -> KwargsT:
        return {
            'hostname': self.hostname, 'username': self.username, 'password': self.password,
            'port': self.port
        }


class SSHRunnerSettings:
    def __init__(self, env: Optional[EnvironmentT] = None,
                 buffering: int = DEFAULT_BUFFERING,
                 is_add_missing_host_keys: bool = True):
        self.env = env
        self.buffering = buffering
        self.is_add_missing_host_keys = is_add_missing_host_keys

    @property
    def exec_kwargs(self) -> KwargsT:
        return {'environment': self.env, 'bufsize': self.buffering}


class SSHRunner(BaseRunner):
    def __init__(self, settings: Optional[SSHRunnerSettings] = None, data_streamer: Optional[DataStreamer] = None):
        self.settings = settings if settings else SSHRunnerSettings()
        self.data_streamer = data_streamer
        self._client = create_client(settings.is_add_missing_host_keys)
        self._connection_details = None

    @property
    def connection_details(self) -> SSHConnectionDetails:
        return self._connection_details

    def connect(self, connection_details: SSHConnectionDetails):
        self._connection_details = connection_details
        self._client.connect(**self._connection_details.connect_kwargs)

    def run(self, command: Union[Command, PrimitiveCommandT]) -> RunOutput:
        if isinstance(command, Command):
            return self._run_command(command)
        return self._run_primitive_command(command)

    def _run_command(self, command: Command) -> RunOutput:
        stdin, stdout, stderr = self._client.exec_command(command.command, timeout=command.timeout,
                                                          **self.settings.exec_kwargs)
        self.data_streamer.stream(source=command.stdin, destination=stdin)
        return RunOutput(stdout=stdout, stderr=stderr, exit_code=stdout.channel.exit_status)

    def _run_primitive_command(self, command: PrimitiveCommandT) -> RunOutput:
        stdin, stdout, stderr = self._client.exec_command(command, **self.settings.exec_kwargs)
        return RunOutput(stdout=stdout, stderr=stderr, exit_code=stdout.channel.exit_status)


def create_client(is_add_missing_host_keys: bool) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    if is_add_missing_host_keys:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    else:
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
    return client
