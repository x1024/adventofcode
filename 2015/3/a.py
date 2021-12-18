#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools


def count_houses(directions):
    houses = set()
    coords = (0, 0)
    deltas = {
        '>': (+1, +0),
        '<': (-1, +0),
        '^': (+0, -1),
        'v': (+0, +1),
    }

    houses.add(coords)
    for d in directions:
        if d not in deltas: continue
        delta = deltas[d]
        coords = (
            coords[0] + delta[0],
            coords[1] + delta[1]
        )
        houses.add(coords)

    return len(houses)


def test():
    assert count_houses('>') == 2
    assert count_houses('^>v<') == 4
    assert count_houses('^v^v^v^v^v') == 2


def main():
    return count_houses(sys.stdin.next())

test()
print main()
