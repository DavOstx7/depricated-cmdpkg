import subprocess
from dataclasses import dataclass
from typing import Optional, BinaryIO
from cmdpkg._typing import EnvironmentT, ProcessInputOutputT, KwargsT


@dataclass
class RunOutput:
    stdout: BinaryIO
    stderr: BinaryIO
    exit_code: int


@dataclass
class RunnerSettings:
    pass


@dataclass
class ProcessRunnerSettings(RunnerSettings):
    env: Optional[EnvironmentT] = None
    cwd: Optional[str] = None
    stdin: Optional[ProcessInputOutputT] = subprocess.PIPE
    stdout: Optional[ProcessInputOutputT] = subprocess.PIPE
    stderr: Optional[ProcessInputOutputT] = subprocess.PIPE

    @property
    def start_process_kwargs(self) -> KwargsT:
        return {
            'env': self.env, 'cwd': self.cwd,
            'stdin': self.stdin, 'stdout': self.stdout, 'stderr': self.stderr
        }


@dataclass
class ShellRunnerSettings(ProcessRunnerSettings):
    @property
    def start_process_kwargs(self) -> KwargsT:
        start_process_kwargs = super().start_process_kwargs
        return {'shell': True, **start_process_kwargs}
