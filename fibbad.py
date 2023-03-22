#!/usr/bin/env python3

# An example of running into the recursion limit while computing Fibonacci
# numbers. This should throw a RecursionError around 1000 calls. The reason why
# we want to try implementing the Fibonacci sequence is because the algorithm
# is not tail recursive, so it would test the generality of the solution.

m = [0, 1]

def f(x: int):
    if len(m) <= x:
        m.append(f(x - 1) + f(x - 2))
    return m[x]

print(f(200))
print(f(2000))
