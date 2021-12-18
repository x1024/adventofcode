#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys


def easy(data, stop_at_first_repeat=False):
    data = [(value[0], int(value[1:])) for value in data.split(", ")]
    pos = (0, 0)
    direction = 0
    seen = set()
    seen.add(tuple(pos))

    def step(pos, dx, dy):
        pos = (pos[0] + dx, pos[1] + dy)
        if stop_at_first_repeat and pos in seen:
            return pos, True
        else:
            seen.add(pos)
        return pos, False

    for turn, distance in data:
        # print pos, turn, distance, seen
        if turn == 'R':
            direction = (direction + 1) % 4
        elif turn == 'L':
            direction = (direction - 1 + 4) % 4
        else:
            raise NotImplementedError()

        dx, dy = 0, 0
        if direction == 0:
            dx = 1
        elif direction == 1:
            dy = 1
        elif direction == 2:
            dx = -1
        elif direction == 3:
            dy = -1
        else:
            raise NotImplementedError()

        for _ in range(distance):
            pos, done = step(pos, dx, dy)
            if done:
                return abs(pos[0]) + abs(pos[1])

    return abs(pos[0]) + abs(pos[1])


def hard(data):
    return easy(data, stop_at_first_repeat=True)


def test():
    assert easy('R2, L3') == 5
    assert easy('R2, R2') == 4
    assert easy('R2, R2, R2') == 2
    assert easy('R2, R2, R2, R2') == 0
    assert easy('R2, R2, R2, R2, R2') == 2
    assert easy('L2, L2') == 4
    assert easy('L2, L2, L2') == 2
    assert easy('L2, L2, L2, L2') == 0
    assert easy('L2, L2, L2, L2, L2') == 2
    assert easy('R5, L5, R5, R3') == 12
    assert hard('R8, R4, R4, R8') == 4


if __name__ == '__main__':
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)

