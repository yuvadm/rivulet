import asyncio
import pytest

from ..batch import BatchProcessor  # Update with your actual import


class TestBatchProcessor:
    @pytest.mark.asyncio
    async def test_batch_by_size(self):
        # Test batching by size
        batch_processor = BatchProcessor[int](
            batch_size=3, timeout_seconds=10.0
        )  # Long timeout

        async def source():
            for i in range(8):  # 8 items should produce 2 full batches and 1 partial
                yield i

        batches = []
        async for batch in batch_processor.process(source()):
            batches.append(batch)

        assert len(batches) == 3
        assert batches[0] == [0, 1, 2]
        assert batches[1] == [3, 4, 5]
        assert batches[2] == [6, 7]

    @pytest.mark.asyncio
    async def test_batch_by_timeout(self):
        # Test batching by timeout
        batch_processor = BatchProcessor[int](
            batch_size=10, timeout_seconds=0.2
        )  # Small timeout

        async def slow_source():
            for i in range(5):
                yield i
                await asyncio.sleep(0.1)  # Fast enough to get multiple items per batch

        batches = []
        async for batch in batch_processor.process(slow_source()):
            batches.append(batch)

        assert len(batches) > 1  # Should have multiple batches due to timeout
        assert (
            sum(len(batch) for batch in batches) == 5
        )  # All items should be processed

    @pytest.mark.asyncio
    async def test_empty_source(self):
        # Test with empty source
        batch_processor = BatchProcessor[int](batch_size=3, timeout_seconds=0.5)

        async def empty_source():
            if False:  # Never yields
                yield 0

        batches = []
        async for batch in batch_processor.process(empty_source()):
            batches.append(batch)

        assert len(batches) == 0  # Should not produce any batches

    @pytest.mark.asyncio
    async def test_exact_batch_size(self):
        # Test with source that produces exactly one full batch
        batch_processor = BatchProcessor[int](batch_size=3, timeout_seconds=0.5)

        async def exact_source():
            for i in range(3):
                yield i

        batches = []
        async for batch in batch_processor.process(exact_source()):
            batches.append(batch)

        assert len(batches) == 1
        assert batches[0] == [0, 1, 2]

    @pytest.mark.asyncio
    async def test_custom_objects(self):
        # Test with custom objects
        class TestItem:
            def __init__(self, value):
                self.value = value

        batch_processor = BatchProcessor[TestItem](batch_size=2, timeout_seconds=0.5)

        async def object_source():
            for i in range(3):
                yield TestItem(i)

        batches = []
        async for batch in batch_processor.process(object_source()):
            batches.append([item.value for item in batch])

        assert len(batches) == 2
        assert batches[0] == [0, 1]
        assert batches[1] == [2]

    @pytest.mark.asyncio
    async def test_concurrent_items(self):
        # Test with items arriving close together but processed in batches
        batch_processor = BatchProcessor[int](batch_size=5, timeout_seconds=0.3)

        async def concurrent_source():
            # Produce items quickly
            for i in range(10):
                yield i
                await asyncio.sleep(0.01)  # Very small delay

            # Then wait (no new items)
            await asyncio.sleep(0.5)

            # Then produce more items quickly
            for i in range(10, 15):
                yield i
                await asyncio.sleep(0.01)

        batches = []
        async for batch in batch_processor.process(concurrent_source()):
            batches.append(batch)

        # Check that we got the expected batches
        assert len(batches) >= 3  # At least 3 batches (could be more due to timing)
        assert sum(len(batch) for batch in batches) == 15  # All items processed

        # Check that first two batches are full size and not timeout-based
        if len(batches) >= 2:
            assert len(batches[0]) == 5
            assert len(batches[1]) == 5
