import pytest

from cmdpkg.commands.utils import pipe_cmds, sum_timeouts


def test_sum_timeouts():
    assert sum_timeouts(1, 2, 3) == 6
    assert sum_timeouts(1, None, 3) == 4
    assert sum_timeouts(None, None, None) is None


def test_pipe_cmds():
    assert pipe_cmds("ab", "cd") == "ab | cd"
    assert pipe_cmds(["a", "b"], ["c", "d"]) == ["a", "b", '|', "c", "d"]


def test_pipe_cmds_raises_type_error():
    with pytest.raises(TypeError):
        pipe_cmds("ab", ["c", "d"])

    with pytest.raises(TypeError):
        pipe_cmds(["a", "b"], "cd")


def test_pipe_cmds_raises_value_error():
    with pytest.raises(ValueError):
        pipe_cmds("ab")

    with pytest.raises(ValueError):
        pipe_cmds(["a", "b"])
