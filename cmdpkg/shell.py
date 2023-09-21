from typing import Optional
from cmdpkg.process import ProcessRunner, ProcessRunnerSettings, KwargsT
from cmdpkg.models import DataStreamer


class ShellRunnerSettings(ProcessRunnerSettings):
    @property
    def start_process_kwargs(self) -> KwargsT:
        return {'shell': True, **super().start_process_kwargs}


class ShellRunner(ProcessRunner):
    def __init__(self, settings: Optional[ShellRunnerSettings] = None, streamer: Optional[DataStreamer] = None):
        settings = settings if settings else ShellRunnerSettings()
        super().__init__(settings, streamer)
