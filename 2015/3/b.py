#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools


def count_houses(directions, houses = None):
    if houses is None:
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


def count_houses_complex(directions):
    houses = set()
    count_houses(directions[::2], houses)
    count_houses(directions[1::2], houses)
    return len(houses)


def test():
    assert count_houses_complex('^v') == 3
    assert count_houses_complex('^>v<') == 3
    assert count_houses_complex('^v^v^v^v^v') == 11


def main():
    return count_houses_complex(sys.stdin.next())


test()
print main()
