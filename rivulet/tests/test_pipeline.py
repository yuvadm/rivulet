import pytest

from ..pipeline import Pipeline


@pytest.mark.asyncio
async def test_pipeline_basic_transformations():
    """Test pipeline with simple transform functions that process values"""

    async def source():
        for i in range(3):
            yield i

    async def double(gen):
        async for value in gen:
            yield value * 2

    async def as_string(gen):
        async for value in gen:
            yield str(value)

    # Create and execute pipeline
    pipeline = Pipeline(source())
    pipeline.add_step(double)
    pipeline.add_step(as_string)

    # Collect results
    results = await pipeline.collect()

    # Verify results
    assert results == ["0", "2", "4"]


@pytest.mark.asyncio
async def test_pipeline_with_expanding_transformations():
    """Test pipeline with a transformation that outputs multiple values per input"""

    async def source():
        yield 1
        yield 2

    async def duplicate(gen):
        async for value in gen:
            yield value
            yield value

    async def multiply_by_ten(gen):
        async for value in gen:
            yield value * 10

    # Test pipeline with expanding transformation first
    pipeline1 = Pipeline(source())
    pipeline1.add_step(duplicate)
    pipeline1.add_step(multiply_by_ten)

    results1 = await pipeline1.collect()
    assert results1 == [10, 10, 20, 20]

    # Test pipeline with expanding transformation last
    pipeline2 = Pipeline(source())
    pipeline2.add_step(multiply_by_ten)
    pipeline2.add_step(duplicate)

    results2 = await pipeline2.collect()
    assert results2 == [10, 10, 20, 20]


@pytest.mark.asyncio
async def test_empty_pipeline():
    """Test pipeline with no transformations"""

    async def source():
        yield "test"

    pipeline = Pipeline(source())
    results = await pipeline.collect()

    assert results == ["test"]


@pytest.mark.asyncio
async def test_pipeline_with_filtering():
    """Test pipeline with a transformation that filters values"""

    async def source():
        for i in range(5):
            yield i

    async def even_only(gen):
        async for value in gen:
            if value % 2 == 0:
                yield value

    pipeline = Pipeline(source())
    pipeline.add_step(even_only)

    results = await pipeline.collect()
    assert results == [0, 2, 4]
