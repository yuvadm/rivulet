import asyncio

from rivulet import Pipeline, Batch


async def source():
    for i in range(22):
        yield i


async def double(gen):
    async for value in gen:
        yield value * 2


async def dump(gen):
    async for x in gen:
        print(x)
        yield x


async def sum(batches):
    async for batch in batches:
        res = 0
        for x in batch:
            res += x
        yield res


async def main():
    pipe = Pipeline(source())
    pipe.add_step(double)

    batch = Batch(N=5, timeout=0.1)
    pipe.add_step(batch)
    pipe.add_step(dump)
    pipe.add_step(sum)

    res = await pipe.collect()
    print(res)


asyncio.run(main())
