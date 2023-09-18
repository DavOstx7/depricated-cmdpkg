from abc import ABC, abstractmethod
from typing import Union, List, BinaryIO, Tuple
from cmdpkg.command import Command, CMDPrimitiveT
from cmdpkg import utils

MIN_RUNNABLES_FOR_PIPE = 2


class RunOutput:
    def __init__(self, stdout: BinaryIO, stderr: BinaryIO, exit_code: int):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code


class BaseRunner(ABC):

    @abstractmethod
    def run(self, runnable: Union[Command, CMDPrimitiveT]) -> RunOutput:
        raise NotImplementedError()

    def run_batch(self, *batch: Union[Command, CMDPrimitiveT]) -> List[RunOutput]:
        outputs = []
        for runnable in batch:
            outputs.append(self.run(runnable))
        return outputs

    def run_pipe(self, *runnable_pipe: Command) -> RunOutput:
        _validate_run_pipe_args(runnable_pipe)
        last_output = self.run(runnable_pipe[0])
        for runnable in runnable_pipe[1:]:
            runnable.stdin = last_output.stdout
            last_output = self.run(runnable)
        return last_output


def _validate_run_pipe_args(runnable_pipe: Tuple[Command]):
    utils.validate_minimum_length(runnable_pipe, MIN_RUNNABLES_FOR_PIPE,
                                  f"Running a pipe requires at least {MIN_RUNNABLES_FOR_PIPE} runnables")
    utils.validate_same_type(runnable_pipe, "Running a pipe requires the runnables to be of the same type")
