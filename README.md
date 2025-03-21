# Rivulet

Lightweight asynchronous data streams.

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

    # or collect them all
    res = await pipe.collect()
```

## License

[MIT](LICENSE)