#!/usr/bin/env python3

# My first attempt at implementing general recursion. I use future callbacks to
# avoid calling f directly which (I thought) would trigger regular infinite
# recursion. The callback pipeline is: x -> ident -> callf -> f -> store
#
# We need ident in order to pass x to callf without calling callf directly
# (which would in turn call f directly). Once store saves the return value of f
# into res, it cancels the infinite loop wait_task and allows wrapped to return
# the result.
#
# Note that in the body of f, the calls to f(x - 1) are actually calling
# wrapped(x - 1), i.e. f is decorated inside the function body.
#
# Pros:
# - General: allows for non-tail recursion
#
# Cons:
# - Tail recursion no longer has constant memory usage
#
# - Inelegant: each recursive call is more like spinning up a subprocess and
#   waiting for I/O than an actual recursive call
#
# - Slow: we have to pass x indirectly through three futures and we have a busy
#   loop that does nothing

import asyncio
from asyncio import Future, CancelledError
from typing import Callable, Coroutine


async def ident(x: int):
    return x


async def forever():
    while True:
        await asyncio.sleep(10)


def recursive(f: Callable[[int], Coroutine]):

    async def wrapped(x: int):
        res = 0
        wait_task = asyncio.create_task(forever())

        def store(fut: Future[int]):
            nonlocal res
            res = fut.result()
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

        return res

    return wrapped


m = [0, 1]


@recursive
async def f(x: int):
    if len(m) <= x:
        m.append(await f(x - 1) + await f(x - 2))
    return m[x]


async def main():
    print(await f(200))
    print(await f(2000))


asyncio.run(main())
