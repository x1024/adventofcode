#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools


def paper(box):
    faces = [a * b for (a, b)
        in itertools.combinations(box, 2)]
    return 2 * sum(faces) + min(faces)


def test():
    assert paper((2, 3, 4)) == 58
    assert paper((1, 1, 10)) == 43


def main():
    return sum(paper(map(int, line.split('x')))
        for line in sys.stdin)

test()
print main()
