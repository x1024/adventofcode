#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import itertools
import sys

def product(array):
    return reduce(lambda a, b: a * b, array)


def easy(data):
    data = list(sorted(map(int, data.split('\n'))))
    total = sum(data) / 3

    for size in range(1, len(data)):
        for c1 in itertools.combinations(data, size):
            if sum(c1) != total:
                continue
            rest = [item for item in data if item not in c1]
            for size2 in range(1, len(rest)):
                for c2 in itertools.combinations(rest, size2):
                    if sum(c2) != total:
                        continue
                    return product(c1)


def hard(data):
    data = list(sorted(map(int, data.split('\n'))))
    total = sum(data) / 4

    data = list(sorted(data))
    for size in range(1, len(data)):
        for c1 in itertools.combinations(data, size):
            if sum(c1) != total:
                continue
            rest = [item for item in data if item not in c1]
            for size2 in range(1, len(rest)):
                for c2 in itertools.combinations(rest, size2):
                    if sum(c2) != total:
                        continue
                    rest2 = [item for item in rest if item not in c2]
                    for size3 in range(1, len(rest2)):
                        for c3 in itertools.combinations(rest2, size3):
                            if sum(c3) != total:
                                continue
                            return product(c1)


def test():
    data = '''1
    2
    3
    4
    5
    7
    8
    9
    10
    11'''
    assert easy(data) == 99
    assert hard(data) == 44


test()
data = sys.stdin.read()
# hp, attack, defense
print easy(data)
print hard(data)
# print hard(stats)
