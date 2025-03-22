# Rivulet

Lightweight building blocks for asynchronous data streams. Provides:

- [x] **Pipeline**: An asynchronous processing chain that connects a data source to a series of transformation steps.
- [x] **Batch**: Accumulates individual stream items into batches of size `N` or when a timeout is reached.
- [ ] **RateLimit**: Controls the flow rate of items through the pipeline by enforcing maximum items per time period constraints.
- [ ] **Parallel**: Executes arbitary steps concurrently across multiple items.
- [ ] **Join**: Combines multiple data streams into a single unified output stream.
- [ ] **Cache**: Stores previously processed results to shortcircuit pipeline steps.

## Installation

Package is not currently published, use directly from source:

```bash
$ uv add git+https://github.com/yuvadm/rivulet.git
```

## Usage

```python
from rivulet import Pipeline, Batch

async def main():
    pipe = Pipeline(source())
    pipe.add_step(double)

    batch = Batch(N=5, timeout=0.1)
    pipe.add_step(batch)
    pipe.add_step(sum)

    # run the pipeline
    async for out in pipe:
        print(out)

    # or just single line it and collect them all
    res = await Pipeline(source(), double, batch, sum).collect()
```

## License

[MIT](LICENSE)