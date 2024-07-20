from typing import Optional
from cmdpkg.process import ProcessRunner, ProcessRunnerSettings, KwargsT
from cmdpkg.models import DataStreamer


class ShellRunnerSettings(ProcessRunnerSettings):
    @property
    def start_process_kwargs(self) -> KwargsT:
        return {'shell': True, **super().start_process_kwargs}


class ShellRunner(ProcessRunner):
    def __init__(self, settings: Optional[ShellRunnerSettings] = None, data_streamer: Optional[DataStreamer] = None):
        super().__init__(settings if settings else ShellRunnerSettings(), data_streamer)
