#!/usr/bin/env python
#-*- coding: UTF-8 -*-


import queue


def solve(number, target=None, limit=None):
    seen = set()
    def is_free(pos):
        if pos in seen: return False
        x, y = pos
        if x < 0 or y < 0: return False
        val = x*x + 3*x + 2*x*y + y + y*y + number
        return bin(val).count("1") % 2 == 0

    # for x in range(20): print ''.join([("." if is_free((y, x)) else "#") for y in range(20)])

    q = queue.Queue()
    q.put((0, (1, 1)))
    offsets = (
        (0, +1),
        (0, -1),
        (+1, 0),
        (-1, 0),
    )

    visited = 0

    while not q.empty():
        steps, pos = q.get()
        if limit and steps > limit:
            return visited

        visited += 1
        if target and pos == target:
            return steps
        seen.add(pos)
        x, y = pos
        for (dx, dy) in offsets:
            p = (x + dx, y + dy)
            if is_free(p):
                seen.add(p)
                q.put((steps + 1, p))


def easy():
    return solve(1358, target=(31, 39))


def hard():
    return solve(1358, limit=50)


def test():
    assert solve(10, target=(7, 4)) == 11


if __name__ == '__main__':
    test()
    # data = sys.stdin.read()
    print easy()
    print hard()