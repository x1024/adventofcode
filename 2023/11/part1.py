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

    print(len(data))
    print(len(data[0]))

    data2 = []
    for row in data:
        data2.append(row)
        if '#' not in row:
            print("ADD")
            data2.append(row)

    print(len(data2))
    print(len(data2[0]))

    data2 = []
    for row in data:
        data2.append(row)
        if '#' not in row:
            data2.append(row)
    data = data2

    data3 = []
    for c in range(len(data[0])):
        col = ''.join(row[c] for row in data)
        data3.append(col)
        if '#' not in col:
            data3.append(col)
    data = data3

    data4 = []
    for c in range(len(data[0])):
        col = ''.join(row[c] for row in data)
        data4.append(col)
    data = data4

    print(len(data))
    print(len(data[0]))
    for row in data:
        print(row)

    result = 0

    stars = []
    for x, row in enumerate(data):
        for y, col in enumerate(row):
            if col == '#':
                stars.append((x, y))

    result = 0
    for i in range(len(stars)):
        for j in range(i+1, len(stars)):
            sa = stars[i]
            sb = stars[j]
            print(sa, sb)
            result += abs(sa[0] - sb[0]) + abs(sa[1] - sb[1])

    print(result)
    return result


data_test = open('input-sample.txt', 'r').read().strip()
result = main(data_test)
print("Test Result: {}".format(result))

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
