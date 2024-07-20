from cmdpkg import utils
from typing import Tuple
from cmdpkg.commands.base import BaseCommand

MIN_COMMANDS_FUR_RUNNING_PIPE = 2


def validate_run_pipe_args(pipe: Tuple[BaseCommand]):
    _validate_run_pipe_args_length(pipe)
    _validate_run_pipe_args_type(pipe)
    for command in pipe[1:]:
        if command.stdin:
            raise ValueError("Running a pipe requires all commands except the first one to not contain stdin")


def _validate_run_pipe_args_length(pipe: Tuple[BaseCommand]):
    if len(pipe) < MIN_COMMANDS_FUR_RUNNING_PIPE:
        raise ValueError(f"Running a pipe requires at least {MIN_COMMANDS_FUR_RUNNING_PIPE} commands")


def _validate_run_pipe_args_type(pipe: Tuple[BaseCommand]):
    if not utils.is_items_instance_of(pipe, BaseCommand):
        raise TypeError(f"Running a pipe requires all commands to be an instance of {BaseCommand.__name__}")
