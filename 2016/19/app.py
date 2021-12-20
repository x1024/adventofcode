#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import functools32 as functools
import math

import sys

def solve(n, k):
    if n == 1: return 1
    return (solve(n - 1, k) + k - 1) % n + 1


def easy(n):
    # https://en.wikipedia.org/wiki/Josephus_problem#k=2
    return 2 * (n - 2 ** int(math.floor(math.log(n, 2)))) + 1


# 1 2 3 4 5 6 7 -> 2 3 5 6 7 1 -> 5
# 1 2 3 4 5 6 -> 2 3 5 6 1 -> 3
# 1 2 3 4 5 -> 2 4 5 1 -> 2
# 1 2 3 4 -> 2 4 1 -> 1 2 -> 1
# 1 2 3 -> 3 1 -> 3
# 1 2 -> 1
# 1 -> 1

# 0 1 2 -> 2 1 -> 0 1 -> 0 -> 2
# 0 1 2 3 4 -> 1 3 4 0
#           -> 0 1 2 3


'''

0
0
2
0
1

0 1 2 -> 2 0
      -> 0 1

'''


@functools.lru_cache(maxsize=100 * 1000 * 1000)
def solve_hard(n):
    if n <= 1: return 0
    i = n // 2

    rest = solve_hard(n - 1)
    # print '!', n, i, rest, rest == n - 2, rest < i - 1
    if rest == n - 2: return 0
    if rest < i - 1: return rest + 1
    return rest + 1 + 1


def hard(n):
    # This is just to prime the cache without blowing up the stack
    for i in range(0, n, sys.getrecursionlimit() / 4):
        print >>sys.stderr, "Cache: %.2f%%" % (float(i) / n * 100)
        solve_hard(i)
    return solve_hard(n) + 1


def test():
    assert easy(5) == 3
    # assert hard(5) == 2


def main():
    test()
    key = 3004953
    print easy(key)
    print hard(key)


if __name__ == '__main__':
    main()