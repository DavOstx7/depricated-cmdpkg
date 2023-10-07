from cmdpkg.commands import utils
from typing import Union, Optional, BinaryIO
from cmdpkg._typing import CMDPrimitiveT


class BaseCommand:
    def __init__(self, cmd: CMDPrimitiveT, timeout: Optional[float] = None, stdin: Optional[BinaryIO] = None):
        self.cmd = cmd
        self.timeout = timeout
        self.stdin = stdin


class Command(BaseCommand):
    def __init__(self, cmd: CMDPrimitiveT, timeout: Optional[float] = None, stdin: Optional[BinaryIO] = None):
        super().__init__(cmd, timeout, stdin)

    def __or__(self, other: Union['Command', CMDPrimitiveT]) -> 'Command':
        if isinstance(other, Command):
            return self._from_piping_command(other)
        return self._from_piping_cmd(other)

    def _from_piping_command(self, other: 'Command') -> 'Command':
        if other.stdin:
            raise ValueError(f"Cannot pipe other command since it contains stdin")
        new_cmd = utils.pipe_cmds(self.cmd, other.cmd)
        new_timeout = utils.sum_timeouts(self.timeout, other.timeout)
        return Command(new_cmd, timeout=new_timeout, stdin=self.stdin)

    def _from_piping_cmd(self, other: CMDPrimitiveT) -> 'Command':
        new_cmd = utils.pipe_cmds(self.cmd, other)
        return Command(new_cmd)

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
