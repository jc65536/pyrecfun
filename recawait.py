#!/usr/bin/env python3

# My first attempt at emulating recursion with future callbacks. Note that this
# method only works for single tail recursion, which is no different than
# iteration.
# 
# Pros:
# - This approach actually uses constant memory. Because wrappedf returns after
#   the new future is dispatched, its parameter (the old future) can be garbage
#   collected. Thus we've brought the long awaited tail recursion optimization
#   to Python!
#
# Cons:
# - The tail recursion is done a rather awkward style where instead of calling
#   f(x + 1) at the end, f returns x + 1 for the callback to receive as its
#   parameter.
#
# - There's no way in Python to wait for all callbacks to complete, which
#   necessitates the `await forever()` line in main. If we comment that line
#   out, main will return before all the callbacks have completed, which halts
#   the counting. Having a non-halting program is certainly no good.

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
