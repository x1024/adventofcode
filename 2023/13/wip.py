import numpy as np
import functools


def difference(pattern, x):
    width = min(x, len(pattern[0]) - x)
    left = [row[x-width:x] for row in pattern]
    right = [row[x:x+width][::-1] for row in pattern]
    return sum(sum(ca != cb for (ca, cb) in zip(a, b)) for a, b in zip(left, right))


def reflections(pattern, diff=0, scale=1):
    return [x * scale for x in range(1, len(pattern[0])) if difference(pattern, x) == diff]


def summarize(pattern, diff=0):
    pattern = list(map(list, pattern))
    transposed = np.rot90(np.array(pattern), 1)
    return reflections(pattern, diff) + reflections(transposed, diff, 100)


data = [pattern.strip().split("\n") for pattern in open('input.txt', 'r').read().strip().split('\n\n')]
print(sum(summarize(p)[0] for p in data))
print(sum(set(summarize(p, 1)).difference(set(summarize(p))).pop() for p in data))

