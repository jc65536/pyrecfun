#!/usr/bin/env python3

import asyncio
from typing import Callable


def recursive(f: Callable[[int], int]):

    async def af(x: int):
        return f(x)

    def wrappedf(fut: asyncio.Future[int]):
        x = fut.result()
        task = asyncio.create_task(af(x))
        task.add_done_callback(wrappedf)
        return task

    def callf(x: int):
        task = asyncio.create_task(af(x))
        task.add_done_callback(wrappedf)
        return task

    return callf


@recursive
def f(x: int):
    print(x)
    return x + 1


async def forever():
    while True:
        await asyncio.sleep(10)


async def main():
    f(0)
    await forever()


asyncio.run(main())
