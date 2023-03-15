#!/usr/bin/env python3

import asyncio
from asyncio import Future, CancelledError
from typing import Callable, Coroutine, Any


class Obj:
    def __init__(self):
        self.x = 0


async def ident(x: int):
    return x


async def forever():
    while True:
        await asyncio.sleep(10)


def recursive(f: Callable[[int], Coroutine[Any, Any, int]]):

    async def wrapped(x: int):
        obj = Obj()
        wait_task = asyncio.create_task(forever())

        def store(fut: Future[int]):
            obj.x = fut.result()
            wait_task.cancel()

        def callf(fut: Future[int]):
            x = fut.result()
            task = asyncio.create_task(f(x))
            task.add_done_callback(store)

        task = asyncio.create_task(ident(x))
        task.add_done_callback(callf)

        try:
            await wait_task
        except CancelledError:
            pass

        return obj.x

    return wrapped


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
