import time
from typing import BinaryIO

NO_BUFFER = -1
LINE_BUFFER = -2

NO_INTERVAL = -1


class DataStreamer:
    def __init__(self, reading_buffer: int = 1024, interval: float = 0.2):
        self.reading_buffer = reading_buffer
        self.interval = interval

    def stream(self, source: BinaryIO, destination: BinaryIO):
        data = self._read_data(source)

        while data:
            destination.write(data)
            destination.flush()
            self._wait()

            data = self._read_data(source)
        destination.close()

    def _wait(self):
        if self.interval != NO_INTERVAL:
            time.sleep(self.interval)

    def _read_data(self, source: BinaryIO):
        if self.reading_buffer == NO_BUFFER:
            return source.read()
        elif self.reading_buffer == LINE_BUFFER:
            return source.readline()
        return source.read(self.reading_buffer)
