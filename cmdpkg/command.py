from typing import Union, List, Optional, BinaryIO, Tuple, Type
from cmdpkg._typing import CMDPrimitiveT
from cmdpkg import utils

MIN_CMDS_FOR_PIPE = 2


def sum_timeouts(*timeouts: Optional[float]) -> Optional[float]:
    timeouts = list(utils.filter_none_values(timeouts))
    if not timeouts:
        return
    return sum(timeouts)


def pipe_cmds(*cmds: CMDPrimitiveT) -> CMDPrimitiveT:
    _validate_pipe_cmds_args_length(cmds)
    if isinstance(cmds[0], str):
        _validate_pipe_cmds_args_type(cmds, str)
        return _pipe_str_cmds(cmds)
    else:
        _validate_pipe_cmds_args_type(cmds, list)
        return _pipe_list_cmds(cmds)


class Command:
    def __init__(self, cmd: CMDPrimitiveT, timeout: Optional[float] = None, stdin: Optional[BinaryIO] = None):
        self.cmd = cmd
        self.timeout = timeout
        self.stdin = stdin

    def __or__(self, other: Union['Command', CMDPrimitiveT]) -> 'Command':
        if isinstance(other, Command):
            return self._from_piping_command(other)
        return self._from_piping_cmd(other)

    def _from_piping_command(self, other: 'Command') -> 'Command':
        if other.stdin:
            raise ValueError(f"Cannot pipe other command since it contains stdin")
        new_timeout = sum_timeouts(self.timeout, other.timeout)
        new_cmd = pipe_cmds(self.cmd, other.cmd)
        return Command(new_cmd, new_timeout, self.stdin)

    def _from_piping_cmd(self, other: CMDPrimitiveT) -> 'Command':
        new_cmd = pipe_cmds(self.cmd, other)
        return Command(new_cmd, self.timeout, self.stdin)

    def __eq__(self, other: Union['Command', CMDPrimitiveT]) -> bool:
        if isinstance(other, Command):
            return self.cmd == other.cmd and self.timeout == other.timeout and self.stdin == other.stdin
        return self.cmd == other

    def __ne__(self, other: Union['Command', CMDPrimitiveT]):
        return not self == other

    def __str__(self) -> str:
        return self.cmd

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.cmd)}, timeout={self.timeout}, stdin={self.stdin})"


def _validate_pipe_cmds_args_length(cmds: Tuple[CMDPrimitiveT]):
    if len(cmds) < MIN_CMDS_FOR_PIPE:
        raise ValueError(f"Piping requires at least {MIN_CMDS_FOR_PIPE} cmds")


def _validate_pipe_cmds_args_type(cmds: Tuple[CMDPrimitiveT], _type: Type[CMDPrimitiveT]):
    if not utils.is_all_items_instance_of(cmds, _type):
        raise TypeError("Piping requires the cmds to be of the same type/subtype")


def _pipe_str_cmds(cmds: Tuple[str]) -> str:
    piped_cmd = ""
    for cmd in cmds:
        piped_cmd += cmd + ' | '
    return piped_cmd[:-3]


def _pipe_list_cmds(cmds: Tuple[List[str]]) -> List[str]:
    piped_cmd = []
    for cmd in cmds:
        piped_cmd += cmd + ['|']
    return piped_cmd[:-1]
