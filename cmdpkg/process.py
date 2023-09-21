import subprocess
from typing import Union, Optional
from cmdpkg._typing import EnvironmentT, ProcessInputOutputT, KwargsT
from cmdpkg.base import BaseRunner, RunOutput, Command, CMDPrimitiveT
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
    def __init__(self, settings: Optional[ProcessRunnerSettings] = None, streamer: Optional[DataStreamer] = None):
        self.settings = settings if settings else ProcessRunnerSettings()
        self.streamer = streamer if streamer else DataStreamer()

    def run(self, runnable: Union[Command, CMDPrimitiveT]) -> RunOutput:
        if isinstance(runnable, Command):
            return self._run_command(runnable)
        return self._run_cmd(runnable)

    def _run_command(self, command: Command) -> RunOutput:
        process = subprocess.Popen(command.cmd, **self.settings.start_process_kwargs)
        if command.stdin:
            self.streamer.stream(source=command.stdin, destination=process.stdin)
        process.wait(command.timeout)
        return RunOutput(stdout=process.stdout, stderr=process.stderr, exit_code=process.returncode)

    def _run_cmd(self, cmd: CMDPrimitiveT) -> RunOutput:
        process = subprocess.Popen(cmd, **self.settings.start_process_kwargs)
        process.wait()
        return RunOutput(stdout=process.stdout, stderr=process.stderr, exit_code=process.returncode)
