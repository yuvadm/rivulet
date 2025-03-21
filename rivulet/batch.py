import time

from typing import AsyncGenerator, AsyncIterable, List, TypeVar, Generic

T = TypeVar("T")
U = TypeVar("U")


class Batch(Generic[T]):
    """
    A processor that batches items from an async generator based on batch size or timeout.

    This can be used as a step in a Pipeline to batch items from the previous step.
    """

    def __init__(self, N: int, timeout: float):
        self.N = N
        self.timeout = timeout

    def __call__(
        self, source: AsyncGenerator[T, None]
    ) -> AsyncGenerator[List[T], None]:
        """
        Make the BatchProcessor callable so it can be added as a step in the Pipeline.

        Args:
            source: The source async generator providing individual items

        Returns:
            An async generator yielding batches of items as lists
        """
        return self.process(source)

    async def process(self, source: AsyncIterable[T]) -> AsyncGenerator[List[T], None]:
        """
        Process items from the source generator into batches.

        Batches are yielded when either:
        1. The batch size is reached
        2. The timeout period has elapsed and there are items in the buffer

        Args:
            source: The source async generator providing individual items

        Yields:
            Lists containing batches of items from the source
        """
        buffer: List[T] = []
        last_flush_time = time.time()

        async for item in source:
            buffer.append(item)

            current_time = time.time()
            timeout_reached = current_time - last_flush_time >= self.timeout
            buffer_full = len(buffer) >= self.N

            if buffer_full or (timeout_reached and buffer):
                yield buffer.copy()  # Yield a copy to avoid mutation issues
                buffer.clear()
                last_flush_time = current_time

        # Don't forget items in buffer when source is exhausted
        if buffer:
            yield buffer
