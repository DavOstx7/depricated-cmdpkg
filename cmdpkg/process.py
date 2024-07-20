import subprocess
from typing import Union, Optional
from cmdpkg._typing import EnvironmentT, ProcessInputOutputT, KwargsT
from cmdpkg._base import BaseRunner, RunOutput, Command, PrimitiveCommandT
from cmdpkg.models import DataStreamer


class ProcessRunnerSettings:
    def __init__(self, env: Optional[EnvironmentT] = None,
                 cwd: Optional[str] = None,
                 stdin: Optional[ProcessInputOutputT] = None,
                 stdout: Optional[ProcessInputOutputT] = None,
                 stderr: Optional[ProcessInputOutputT] = None):
        self.env = env
        self.cwd = cwd
        self.stdin = stdin if stdin else subprocess.PIPE
        self.stdout = stdout if stdin else subprocess.PIPE
        self.stderr = stderr if stdin else subprocess.PIPE

    @property
    def start_process_kwargs(self) -> KwargsT:
        return {
            'env': self.env, 'cwd': self.cwd,
            'stdin': self.stdin, 'stdout': self.stdout, 'stderr': self.stderr
        }


class ProcessRunner(BaseRunner):
    def __init__(self, settings: Optional[ProcessRunnerSettings] = None, data_streamer: Optional[DataStreamer] = None):
        self.settings = settings if settings else ProcessRunnerSettings()
        self.data_streamer = data_streamer if data_streamer else DataStreamer()

    def run(self, command: Union[Command, PrimitiveCommandT]) -> RunOutput:
        if isinstance(command, Command):
            return self._run_command(command)
        return self._run_primitive_command(command)

    def _run_command(self, command: Command) -> RunOutput:
        process = subprocess.Popen(command.command, **self.settings.start_process_kwargs)
        if command.stdin:
            self.data_streamer.stream(source=command.stdin, destination=process.stdin)
        process.wait(command.timeout)
        return RunOutput(stdout=process.stdout, stderr=process.stderr, exit_code=process.returncode)

    def _run_primitive_command(self, command: PrimitiveCommandT) -> RunOutput:
        process = subprocess.Popen(command, **self.settings.start_process_kwargs)
        process.wait()
        return RunOutput(stdout=process.stdout, stderr=process.stderr, exit_code=process.returncode)
