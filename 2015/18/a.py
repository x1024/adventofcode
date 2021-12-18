#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools


def iterate(rows):
    n = len(rows[0])
    m = len(rows)
    new_data = []
    for i in range(0, m):
        new_data.append([0] * n)

    for i in range(1, m - 1):
        for j in range(1, n - 1):
            total = (
                rows[i+1][j+1] + 
                rows[i+1][j+0] + 
                rows[i+1][j-1] + 

                rows[i+0][j+1] + 
                rows[i+0][j-1] + 

                rows[i-1][j+1] + 
                rows[i-1][j+0] + 
                rows[i-1][j-1]
            )
            if rows[i][j] == 1:
                if total <= 1 or total >= 4:
                    new_data[i][j] = 0
                else:
                    new_data[i][j] = 1
            else:
                if total == 3:
                    new_data[i][j] = 1
                else:
                    new_data[i][j] = 0
    return new_data


def easy(data, iterations, limit_corners = False):
    rows = data.split('\n')
    rows = [list(row) for row in rows if row]
    n = len(rows[0])
    m = len(rows)

    array = []
    for i in range(m + 2):
        array.append([0] * (n+2))

    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            # print i, j, col, col == '#', int(col == '#')
            array[i + 1][j + 1] = int(col == '#')

    if limit_corners:
        array[1][1] = 1
        array[1][n] = 1
        array[m][1] = 1
        array[m][n] = 1

    for i in range(iterations):
        array = iterate(array)
        if limit_corners:
            array[1][1] = 1
            array[1][n] = 1
            array[m][1] = 1
            array[m][n] = 1

    return sum(sum(row) for row in array)


def hard(data, iterations):
    return easy(data, iterations, limit_corners=True)


def test():
    data = '''
.#.#.#
...##.
#....#
..#...
#.#..#
####..
'''
    assert easy(data, 4) == 4
    assert hard(data, 5) == 17


test()
data = '\n'.join(list(sys.stdin))
# print data
print easy(data, 100)
print hard(data, 100)
