#!/usr/bin/env python3

import asyncio
from typing import Callable, Coroutine, Any


def recursive(f: Callable[[int], Coroutine[Any, Any, Any]]):

    async def callf(x: int):
        return await asyncio.create_task(f(x))

    return callf


m: dict[int, int] = {}


@recursive
async def f(x: int):
    if x == 0 or x == 1:
        return x
    elif x in m:
        return m[x]
    m[x] = await f(x - 1) + await f(x - 2)
    return m[x]


async def main():
    print(await f(200))
    print(await f(2000))


asyncio.run(main())
