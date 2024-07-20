from abc import ABC, abstractmethod
from typing import Union, List, BinaryIO
from cmdpkg import utils
from cmdpkg.command import Command, PrimitiveCommandT


class RunOutput:
    def __init__(self, stdout: BinaryIO, stderr: BinaryIO, exit_code: int):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code


class BaseRunner(ABC):
    @abstractmethod
    def run(self, command: Union[Command, PrimitiveCommandT]) -> RunOutput:
        raise NotImplementedError()

    def run_batch(self, *batch: Union[Command, PrimitiveCommandT]) -> List[RunOutput]:
        outputs = []
        for command in batch:
            outputs.append(self.run(command))
        return outputs

    def run_pipe(self, *pipe: Command) -> RunOutput:
        utils.validate_minimum_length(commands_pipe, 2, "Running a pipe requires to provide at least 2 arguments")
        last_output = self.run(commands_pipe[0])
        for current_command in commands_pipe[1:]:
            current_command.stdin = last_output.stdout
            last_output = self.run(current_command)
        return last_output
