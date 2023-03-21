#!/usr/bin/env python3

import asyncio
from fibawait2 import recursive

@recursive
async def f(x: int):
    print(x)
    await f(x + 1)

asyncio.run(f(0))
