#!/usr/bin/env python3

m = [0, 1]

def f(x: int):
    for i in range(len(m), x + 1):
        m.append(m[i - 1] + m[i - 2])
    return m[x]
    
print(f(200))
print(f(2000))
