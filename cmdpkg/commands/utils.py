from cmdpkg import utils
from typing import List, Optional, Tuple, Type
from cmdpkg._typing import CMDPrimitiveT

MIN_CMDS_FOR_PIPING = 2


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


def _validate_pipe_cmds_args_length(cmds: Tuple[CMDPrimitiveT]):
    if len(cmds) < MIN_CMDS_FOR_PIPING:
        raise ValueError(f"Piping requires at least {MIN_CMDS_FOR_PIPING} cmds")


def _validate_pipe_cmds_args_type(cmds: Tuple[CMDPrimitiveT], _type: Type[CMDPrimitiveT]):
    if not utils.is_items_instance_of(cmds, _type):
        raise TypeError(f"Piping requires all cmds to be an instance of {_type}")


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
