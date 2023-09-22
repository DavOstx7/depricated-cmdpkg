from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union, List, BinaryIO, Tuple
from cmdpkg.command import Command, CMDPrimitiveT
from cmdpkg import utils

MIN_RUNNABLES_FOR_PIPE = 2


@dataclass
class RunOutput:
    stdout: BinaryIO
    stderr: BinaryIO
    exit_code: int


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
    _validate_run_pipe_args_length(runnable_pipe)
    _validate_run_pipe_args_type(runnable_pipe)
    for runnable in runnable_pipe[1:]:
        if runnable.stdin:
            raise ValueError("Running a pipe requires all runnable except the first one to not contain stdin")


def _validate_run_pipe_args_length(runnable_pipe: Tuple[Command]):
    if len(runnable_pipe) < MIN_RUNNABLES_FOR_PIPE:
        raise ValueError(f"Running a pipe requires at least {MIN_RUNNABLES_FOR_PIPE} runnables")


def _validate_run_pipe_args_type(runnable_pipe: Tuple[Command]):
    if not utils.is_all_items_instance_of(runnable_pipe, Command):
        raise TypeError("Running a pipe requires all the runnables to be an instance of Command")
