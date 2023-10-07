from typing import Optional
from cmdpkg.runners.process import ProcessRunner
from cmdpkg.runners.models import ShellRunnerSettings
from cmdpkg.models import DataStreamer


class ShellRunner(ProcessRunner):
    def __init__(self, settings: Optional[ShellRunnerSettings] = None, streamer: Optional[DataStreamer] = None):
        settings = settings if settings else ShellRunnerSettings()
        super().__init__(settings, streamer)
