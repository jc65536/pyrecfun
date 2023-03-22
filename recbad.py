#!/usr/bin/env python3

# An example of running into the recursion limit in Python. This should throw a
# RecursionError around 1000 calls.

def f(x: int):
    print(x)
    f(x + 1)

f(0)
