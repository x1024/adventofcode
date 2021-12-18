#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys


def clamp(val, vmin, vmax):
    return min(vmax, max(vmin, val))

deltas = {
    'U': (-1, 0),
    'D': (+1, 0),
    'L': (0, -1),
    'R': (0, +1),
}


def make_pos(pos, delta, keypad):
    new_pos = (clamp(pos[0] + delta[0], 0, len(keypad) - 1),
                clamp(pos[1] + delta[1], 0, len(keypad[0]) - 1))
    if keypad[new_pos[0]][new_pos[1]] == '0':
        return pos
    return new_pos


def solve(data, keypad, starting_pos):
    return ''.join(keypad[pos[0]][pos[1]]
        for pos in reduce(
            lambda result, row:
                result + [reduce(lambda pos, delta: make_pos(pos, delta, keypad),
                    (deltas[cell] for cell in row),
                    result[-1])],
            data.split('\n'),
            [starting_pos])[1:])


def easy(data):
    keypad = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]

    return solve(data, keypad, (1, 1))


def hard(data):
    keypad = [
        ['0','0','1','0','0'],
        ['0','2','3','4','0'],
        ['5','6','7','8','9'],
        ['0','A','B','C','0'],
        ['0','0','D','0','0'],
    ]
    return solve(data, keypad, (2, 0))


def test():
    data = '''ULL
RRDDD
LURDL
UUUUD'''
    assert easy(data) == '1985'
    assert hard(data) == '5DB3'


if __name__ == '__main__':
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)

