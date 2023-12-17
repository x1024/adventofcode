import collections
import numpy
import pprint
import re
import functools
import itertools
import numpy as np

def rotate_matrix( m ):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]


def main(data):
    # pprint.pprint(data)
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = list(map(int, data))

    empty_rows = []
    empty_columns = []

    data2 = []
    for i, row in enumerate(data):
        if '#' not in row:
            empty_rows.append(i)

    for c in range(len(data[0])):
        col = [row[c] for row in data]
        if '#' not in col:
            empty_columns.append(c)

    print(empty_rows)
    print(empty_columns)

    result = 0

    stars = []
    for x, row in enumerate(data):
        for y, col in enumerate(row):
            if col == '#':
                stars.append((x, y))

    result = 0
    mult = 1000000 - 1
    def transform(point):
        x, y = point
        er = sum(1 for i in empty_rows if i < x)
        ec = sum(1 for i in empty_columns if i < y)
        return x + er * mult, y + ec * mult

    for i in range(len(stars)):
        for j in range(i+1, len(stars)):
            sa = transform(stars[i])
            sb = transform(stars[j])
            result += abs(sa[0] - sb[0]) + abs(sa[1] - sb[1])

    # print(result)
    return result


data_test = open('input-sample.txt', 'r').read().strip()
result = main(data_test)
print("Test Result: {}".format(result))
# exit()

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
