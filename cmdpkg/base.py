from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union, List, BinaryIO, Tuple
from cmdpkg.command import Command, CMDPrimitiveT
from cmdpkg import utils

MIN_COMMANDS_FOR_PIPE = 2


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

    def run_pipe(self, *pipe: Command) -> RunOutput:
        _validate_run_pipe_args(pipe)
        last_output = self.run(pipe[0])
        for command in pipe[1:]:
            command.stdin = last_output.stdout
            last_output = self.run(command)
        return last_output


def _validate_run_pipe_args(pipe: Tuple[Command]):
    _validate_run_pipe_args_length(pipe)
    _validate_run_pipe_args_type(pipe)
    for command in pipe[1:]:
        if command.stdin:
            raise ValueError("Running a pipe requires all commands except the first one to not contain stdin")


def _validate_run_pipe_args_length(pipe: Tuple[Command]):
    if len(pipe) < MIN_COMMANDS_FOR_PIPE:
        raise ValueError(f"Running a pipe requires at least {MIN_COMMANDS_FOR_PIPE} commands")


def _validate_run_pipe_args_type(pipe: Tuple[Command]):
    if not utils.is_items_instance_of(pipe, Command):
        raise TypeError("Running a pipe requires all the commands to be an instance of Command")
