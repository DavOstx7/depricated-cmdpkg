import subprocess
from typing import Union, Optional
from cmdpkg.runners.base import BaseRunner, RunOutput, BaseCommand, CMDPrimitiveT
from cmdpkg.runners.models import ProcessRunnerSettings
from cmdpkg.models import DataStreamer


class ProcessRunner(BaseRunner):
    def __init__(self, settings: Optional[ProcessRunnerSettings] = None, streamer: Optional[DataStreamer] = None):
        self.settings = settings if settings else ProcessRunnerSettings()
        self.streamer = streamer if streamer else DataStreamer()

    def run(self, runnable: Union[BaseCommand, CMDPrimitiveT]) -> RunOutput:
        if isinstance(runnable, BaseCommand):
            return self._run_command(runnable)
        return self._run_cmd(runnable)

    def _run_command(self, command: BaseCommand) -> RunOutput:
        process = subprocess.Popen(command.cmd, **self.settings.start_process_kwargs)
        if command.stdin:
            self.streamer.stream(source=command.stdin, destination=process.stdin)
        process.wait(command.timeout)
        return RunOutput(stdout=process.stdout, stderr=process.stderr, exit_code=process.returncode)

    def _run_cmd(self, cmd: CMDPrimitiveT) -> RunOutput:
        process = subprocess.Popen(cmd, **self.settings.start_process_kwargs)
        process.wait()
        return RunOutput(stdout=process.stdout, stderr=process.stderr, exit_code=process.returncode)
