#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools
from functools import reduce


def product(lst):
    return reduce((lambda x, y: x * y), lst)


def ribbon(box):
    perimeters = [2 * (a + b) for (a, b)
        in itertools.combinations(box, 2)]
    volume = product(box)
    return min(perimeters) + volume


def test():
    assert ribbon((2, 3, 4)) == 34
    assert ribbon((1, 1, 10)) == 14


def main():
    return sum(ribbon(map(int, line.split('x')))
        for line in sys.stdin)

test()
print main()
