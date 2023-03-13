#!/usr/bin/env python3

def f(x: int):
    print(x)
    f(x + 1)

f(0)
