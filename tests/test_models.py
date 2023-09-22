import pytest
from unittest.mock import patch, Mock, call

import random
from cmdpkg.models import DataStreamer, LINE_BUFFER, NO_BUFFER, NO_INTERVAL


@pytest.fixture(scope="module")
def buffer() -> int:
    return random.choice([random.randint(1, 1024), LINE_BUFFER, NO_BUFFER])


@pytest.fixture(scope="module")
def interval() -> float:
    return random.choice([random.uniform(1, 100), NO_INTERVAL])


class TestDataStreamer:
    def test_read_data_with_buffer(self, binary_io_factory):
        data_streamer = DataStreamer(reading_buffer=1024)
        source = binary_io_factory()
        return_value = data_streamer._read_data(source)

        source.read.assert_called_once_with(1024)
        assert return_value == source.read.return_value

    def test_read_data_with_line_buffer(self, binary_io_factory):
        data_streamer = DataStreamer(reading_buffer=LINE_BUFFER)
        source = binary_io_factory()
        return_value = data_streamer._read_data(source)

        source.readline.assert_called_once_with()
        assert return_value == source.readline.return_value

    def test_read_data_without_buffer(self, binary_io_factory):
        data_streamer = DataStreamer(reading_buffer=NO_BUFFER)
        source = binary_io_factory()
        return_value = data_streamer._read_data(source)

        source.read.assert_called_once_with()
        assert return_value == source.read.return_value

    @patch('time.sleep')
    def test_wait_with_interval(self, sleep_mock: Mock):
        data_streamer = DataStreamer(interval=0.2)

        data_streamer._wait()

        sleep_mock.assert_called_once_with(0.2)

    @patch('time.sleep')
    def test_wait_without_interval(self, sleep_mock: Mock, interval):
        data_streamer = DataStreamer(interval=NO_INTERVAL)

        data_streamer._wait()

        sleep_mock.assert_not_called()

    @patch.object(DataStreamer, '_wait')
    @patch.object(DataStreamer, '_read_data')
    def test_stream(self, read_data_mock: Mock, wait_mock: Mock, buffer, interval, binary_io_factory):
        source, destination = binary_io_factory(), binary_io_factory()
        read_data_mock.side_effect = ["a", "b", ""]
        data_streamer = DataStreamer(buffer, interval)

        data_streamer.stream(source, destination)

        read_data_mock.assert_has_calls([call(source), call(source), call(source)])
        destination.write.assert_has_calls([call("a"), call("b")])
        destination.flush.assert_has_calls([call(), call()])
        wait_mock.assert_has_calls([call(), call()])

        destination.close.assert_called_once_with()
