#!/usr/bin/env python3

import asyncio
from typing import Callable


def recursive(f: Callable[[int], int]):

    def wrap(fut: asyncio.Future[int]):
        x = fut.result()
        res = f(x)
        fut = asyncio.Future()
        fut.add_done_callback(wrap)
        fut.set_result(res)
        return res

    def callf(x: int):
        fut = asyncio.Future()
        fut.set_result(x)
        wrap(fut)

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
