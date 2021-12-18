#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import itertools
import sys

def product(array):
    return reduce(lambda a, b: a * b, array)



def next_code(code):
    return (code * 252533) % 33554393


def sum_n(n):
    return n * (n + 1) / 2


def position(row, column):
    row_x_column_1 = sum_n(row) - (row - 1)
    row_x_column_y = row_x_column_1 + sum_n(column + row - 1) - sum_n(row)
    return row_x_column_y 


def easy(row, column):
    code = 20151125
    index = 1

    pos = position(row, column)
    # print pos
    # print row, column
    # print index, code
    while index < pos:
        code = next_code(code)
        index += 1
        # if index % 100 == 0: print float(index) / pos, index, code
    # print float(index) / pos, index, code
    return code


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
    assert position(1, 1) == 1
    assert position(2, 1) == 2
    assert position(1, 2) == 3
    assert position(3, 3) == 13
    assert position(3, 4) == 19
    assert position(1, 6) == 21
    print 'test done'

    # assert easy(4, 1) == 99
    # assert hard(data) == 44


test()
# data = sys.stdin.read()
# hp, attack, defense
print easy(3010, 3019)
# print hard(data)
# print hard(stats)
