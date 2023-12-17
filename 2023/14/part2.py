import collections
import numpy
import pprint
import re
import functools
import itertools


def print_map(map):
    rows = int(max(c.real for c in map.keys()))
    cols = int(max(c.imag for c in map.keys()))

    for i in range(rows + 1):
        for j in range(cols + 1):
            coord = (j + i * 1j)
            print(map[coord], end='')
        print()

def tilt(map, direction=(0 - 1j)):
    moved = False
    for coord, val in map.items():
        if val == 'O':
            while True:
                new_coord = coord + direction
                if map.get(new_coord, None) == '.':
                    map[new_coord] = 'O'
                    map[coord] = '.'
                    moved = True
                else:
                    break
    if moved:
        map = tilt(map, direction)
    return map

def cycle(map):
    map = tilt(map, (+0 - 1j))
    map = tilt(map, (-1 + 0j))
    map = tilt(map, (+0 + 1j))
    map = tilt(map, (+1 + 0j))
    return map

def value(map):
    rows = int(max(c.real for c in map.keys())) + 1
    result = 0
    for coord, val in map.items():
        if val == 'O':
            r = rows - int(coord.imag)
            result += r
            print(coord, rows, r)
    return result


def main(data):
    # pprint.pprint(data)
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))
    print(data)
    map = {}
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            coord = (c + r * 1j)
            map[coord] = col
            # if col == 'O':
            # elif col == '#':
            # else:

    seen = {}

    LIMIT = 1000000000
    x = 0
    while x < LIMIT:
        key = tuple(map.items())
        if key in seen:
            print("Found", x, seen[key])
            period = x - seen[key]
            print("Period", period)
            while x + period < LIMIT:
                x += period
            print(x)
        seen[key] = x

        map = cycle(map)
        print(x)
        x += 1

    return (value(map))


    result = 0


    # for x in range(0, 100):
    



    print(result)
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
