import time
from typing import BinaryIO

LINE_BUFFER = -1


class DataStreamer:
    def __init__(self, reading_buffer: int = 1024, interval: float = 0.2):
        self.reading_buffer = reading_buffer
        self.interval = interval

    def stream(self, source: BinaryIO, destination: BinaryIO):
        data = self._read_data(source)

        while data:
            destination.write(data)
            destination.flush()
            time.sleep(self.interval)

            data = self._read_data(source)
        destination.close()

    def _read_data(self, source: BinaryIO):
        if self.reading_buffer == LINE_BUFFER:
            return source.readline()
        return source.read(self.reading_buffer)
