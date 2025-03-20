# Rivulet

Elegant asynchronous data streams

```python
from rivulet import BatchProcessor

async def item_stream():
    for i in range(10):
        yield i
        await asyncio.sleep(0.1)

async def main():
    processor = BatchProcessor(batch_size=3, timeout_seconds=0.5)
    
    async for batch in processor.process(item_stream()):
        print(f"Processing batch of {len(batch)} items: {batch}")
```