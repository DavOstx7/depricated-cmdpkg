from cmdpkg.runners import utils
from abc import ABC, abstractmethod
from typing import Union, List
from cmdpkg._typing import CMDPrimitiveT
from cmdpkg.commands.base import BaseCommand
from cmdpkg.runners.models import RunOutput

MIN_COMMANDS_FOR_PIPE = 2


class IRunner(ABC):
    @abstractmethod
    def run(self, runnable: Union[BaseCommand, CMDPrimitiveT]) -> RunOutput:
        raise NotImplementedError()


class BaseRunner(IRunner, ABC):
    def run_batch(self, *batch: Union[BaseCommand, CMDPrimitiveT]) -> List[RunOutput]:
        outputs = []
        for runnable in batch:
            outputs.append(self.run(runnable))
        return outputs

    def run_pipe(self, *pipe: BaseCommand) -> RunOutput:
        utils.validate_run_pipe_args(pipe)
        last_output = self.run(pipe[0])
        for command in pipe[1:]:
            command.stdin = last_output.stdout
            last_output = self.run(command)
        return last_output
