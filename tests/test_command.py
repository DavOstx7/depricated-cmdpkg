import pytest
from cmdpkg.command import Command


def test_equaling_command(fake_binary_io):
    assert Command('1') == Command('1')
    assert not Command('1') == Command('2')
    assert not Command('1', timeout=1) == Command('1')
    assert not Command('1', stdin=fake_binary_io) == Command('1')
    assert Command('1', timeout=1, stdin=fake_binary_io) == Command('1', timeout=1, stdin=fake_binary_io)


def test_piping_command():
    assert Command("echo abc") | Command("findstr a") == Command("echo abc | findstr a", timeout=None, stdin=None)

    assert Command(['echo', 'abc']) | Command(['findstr', 'a']) == \
           Command(['echo', 'abc', '|', 'findstr', 'a'], timeout=None, stdin=None)

    with pytest.raises(AssertionError):
        _ = Command("echo abc") | Command(['findstr', 'a'])

    with pytest.raises(AssertionError):
        _ = Command(['echo', 'abc']) | Command("findstr a")


def test_piping_with_timeout():
    assert Command("echo abc", timeout=1) | Command("findstr a", timeout=2) == \
           Command("echo abc | findstr a", timeout=3, stdin=None)

    assert Command(['echo', 'abc'], timeout=1) | Command(['findstr', 'a'], timeout=2) == \
           Command(['echo', 'abc', '|', 'findstr', 'a'], timeout=3, stdin=None)


def test_piping_command_with_stdin(fake_binary_io):
    assert Command("echo abc", stdin=fake_binary_io) | Command("findstr a") == \
           Command("echo abc | findstr a", timeout=None, stdin=fake_binary_io)

    assert Command(['echo', 'abc'], stdin=fake_binary_io) | Command(['findstr', 'a']) == \
           Command(['echo', 'abc', '|', 'findstr', 'a'], timeout=None, stdin=fake_binary_io)

    with pytest.raises(ValueError):
        _ = Command("echo abc") | Command("findstr a", stdin=fake_binary_io)

    with pytest.raises(ValueError):
        _ = Command(['echo', 'abc']) | Command(['findstr', 'a'], stdin=fake_binary_io)
