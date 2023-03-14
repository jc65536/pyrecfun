#!/usr/bin/env python3

import asyncio
from asyncio import AbstractEventLoop
from typing import Callable


def recursive(f: Callable[[int], int]):
    loop: AbstractEventLoop

    def wrappedf(fut: asyncio.Future[int]):
        x = fut.result()
        res = f(x)
        fut = loop.create_future()
        fut.add_done_callback(wrappedf)
        fut.set_result(res)
        return res

    def callf(x: int):
        nonlocal loop
        loop = asyncio.get_event_loop()
        fut = loop.create_future()
        fut.set_result(x)
        wrappedf(fut)

    return callf


@recursive
def f(x: int):
    print(x)
    return x + 1


async def main():
    f(0)
    while True:
        await asyncio.sleep(10)

asyncio.run(main())
