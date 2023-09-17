import pytest
from unittest.mock import patch, Mock, call

import random

from cmdpkg.models import DataStreamer


@pytest.fixture(scope="module")
def buffer() -> int:
    return random.randint(1, 1024)


@pytest.fixture(scope="module")
def interval() -> float:
    return random.uniform(1, 100)


def test_streamer_read_data_size_buffer(buffer, binary_io_factory):
    data_streamer = DataStreamer(reading_buffer=buffer)
    source = binary_io_factory()
    return_value = data_streamer._read_data(source)

    source.read.assert_called_once_with(buffer)
    assert return_value == source.read.return_value


def test_streamer_read_data_line_buffer(binary_io_factory):
    data_streamer = DataStreamer(reading_buffer=-1)
    source = binary_io_factory()
    return_value = data_streamer._read_data(source)

    source.readline.assert_called_once_with()
    assert return_value == source.readline.return_value


@patch('time.sleep')
@patch.object(DataStreamer, '_read_data')
def test_streamer_stream(read_data_mock: Mock, sleep_mock: Mock, buffer, interval, binary_io_factory):
    source, destination = binary_io_factory(), binary_io_factory()
    read_data_mock.side_effect = ["a", "b", ""]
    data_streamer = DataStreamer(buffer, interval)

    data_streamer.stream(source, destination)

    read_data_mock.assert_has_calls([call(source), call(source), call(source)])
    destination.write.assert_has_calls([call("a"), call("b")])
    destination.flush.assert_has_calls([call(), call()])
    sleep_mock.assert_has_calls([call(interval), call(interval)])

    destination.close.assert_called_once_with()
