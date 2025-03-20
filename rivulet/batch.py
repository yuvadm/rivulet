import time

from typing import TypeVar, Generic, AsyncIterable, AsyncIterator, List


T = TypeVar("T")


class BatchProcessor(Generic[T]):
    def __init__(self, batch_size: int, timeout_seconds: float):
        self.batch_size = batch_size
        self.timeout_seconds = timeout_seconds

    async def process(self, source: AsyncIterable[T]) -> AsyncIterator[List[T]]:
        buffer: List[T] = []
        last_flush_time = time.time()

        async for item in source:
            buffer.append(item)

            current_time = time.time()
            timeout_reached = current_time - last_flush_time >= self.timeout_seconds
            buffer_full = len(buffer) >= self.batch_size

            if buffer_full or (timeout_reached and buffer):
                yield buffer
                buffer = []
                last_flush_time = current_time

        # Don't forget items in buffer when source is exhausted
        if buffer:
            yield buffer
