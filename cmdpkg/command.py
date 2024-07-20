from typing import Union, List, Optional, BinaryIO, Tuple
from cmdpkg._typing import PrimitiveCommandT
from cmdpkg import utils


class Command:
    def __init__(self, command: PrimitiveCommandT, timeout: Optional[float] = None, stdin: Optional[BinaryIO] = None):
        self.command = command
        self.timeout = timeout
        self.stdin = stdin

    def __or__(self, other: Union['Command', PrimitiveCommandT]) -> 'Command':
        if isinstance(other, Command):
            return self._pipe_command(other)
        return self._pipe_primitive_command(other)

    def _pipe_command(self, other: 'Command') -> 'Command':
        if other.stdin:
            raise ValueError(f"Cannot pipe other runnable since it contains stdin")
        new_timeout = sum_timeouts(self.timeout, other.timeout)
        new_command = pipe_commands(self.command, other.command)
        return self._from_params(command=new_command, timeout=new_timeout, stdin=self.stdin)

    def _pipe_primitive_command(self, other: PrimitiveCommandT) -> 'Command':
        new_command = pipe_commands(self.command, other)
        return self._from_params(command=new_command, timeout=self.timeout, stdin=self.stdin)

    @classmethod
    def _from_params(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __eq__(self, other: Union['Command', PrimitiveCommandT]) -> bool:
        if isinstance(other, Command):
            return self.command == other.command and self.timeout == other.timeout and self.stdin == other.stdin
        return self.command == other

    def __str__(self) -> str:
        return f"{type(self).__name__}({repr(self.command)})"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.command)}, timeout={self.timeout}, stdin={self.stdin})"


def sum_timeouts(*timeouts: Optional[float]) -> Optional[float]:
    timeouts = list(utils.filter_none_values(timeouts))
    if not timeouts:
        return
    return sum(timeouts)


def pipe_commands(*commands: PrimitiveCommandT) -> PrimitiveCommandT:
    _validate_pipe_commands_args(commands)
    if isinstance(commands[0], str):
        return _pipe_str_commands(commands)
    else:
        return _pipe_list_commands(commands)


def _validate_pipe_commands_args(commands: Tuple[PrimitiveCommandT]):
    utils.validate_minimum_length(commands, 2, "Piping requires to provide at least 2 arguments")
    utils.validate_same_type(commands, "Piping requires the provided arguments to be of the same type")


def _pipe_str_commands(commands: Tuple[str]) -> str:
    piped_command = ""
    for current_command in commands:
        piped_command += current_command + ' | '
    return piped_command[:-3]


def _pipe_list_commands(commands: Tuple[List[str]]) -> List[str]:
    piped_command = []
    for current_command in commands:
        piped_command += current_command + ['|']
    return piped_command[:-1]


class CommandA(Command):
    pass


print(repr(CommandA("a", timeout=2) | Command("c")))
