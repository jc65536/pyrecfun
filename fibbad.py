#!/usr/bin/env python3

m = [0, 1]

def f(x: int):
    if len(m) <= x:
        m.append(f(x - 1) + f(x - 2))
    return m[x]

print(f(200))
print(f(2000))
