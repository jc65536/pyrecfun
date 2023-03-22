#!/usr/bin/env python3

# While fiddling around with the implementation in fibawait.py, I realized that
# we could actually remove a lot of redundant code. Eventually, I deleted
# deleted all of that future callback clutter and was left with this one-liner
# implementation.
#
# What surprised me the most was that apparently writing f(x) directly does not
# lead to regular infinite recursion! Here I will try to explain why that
# happens. Note: in f and main (basically everywhere outside recursive), f
# actually refers to the decorated f, i.e. the lambda, which I will notate here
# as @f.
#
# My first hypothesis:
# - When main calls @f, it first calls f(x) because Python is eagerly evaluated
# - After entering the if statement, f calls @f(x - 1)
#
# Wait, shouldn't this lead to regular infinite recursion? After stepping
# through the code with a debugger, I found out that asyncio.create_task is
# somehow able to immediately get a coroutine. I'm not sure how this works, but
# if you write a my_create_task function that's just a wrapper for
# asyncio.create_task, you can see that @f steps directly into my_create_task
# with a coroutine in the arguments. My assumption that @f would evaluate f(x)
# first was incorrect.
#
# In reality, we do not enter the body of f when we call f(x). Instead, it just
# returns a coroutine. It's when we await the coroutine that the body of f is
# actually executed.
#
# https://stackoverflow.com/questions/75808091/python-skips-coroutine-evaluation
#
# Pros
# - Simple!
# - Much more efficient than the fibawait.py implementation
#
# Cons
# - Not optimized for tail recursion

import asyncio
from typing import Callable, Coroutine


def recursive(f: Callable[[int], Coroutine]):
    return lambda x: asyncio.create_task(f(x))


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
