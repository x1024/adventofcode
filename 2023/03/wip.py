import functools
import collections
import numpy
import pprint
import re

ADJACENT = [
    x + 1j * y for x in [-1,0,1] for y in [-1,0,1]
]

def solve(data):
    def is_part(pos):
        v = data.get(pos, None)
        if v is None: return False
        return (v < '0' or v > '9') and v != '.'

    total = 0
    numbers = {}
    print(data)
    for pos in data:
        print(pos)

    exit()
    for pos in data:
    for x in range(len(data)):
        for number in re.finditer('\d+', data[x]):
            s, e = number.span()
            value = number.group(0)
            for y in range(s, e):
                numbers[(x, y)] = value

            if any(is_part(pos + offset) for offset in ADJACENT):
                total += int(value)

    total2 = 0
    for x in range(len(data)):
        for y in range(len(data[x])):
            if data[x][y] != '*': continue
            values = set(
                numbers.get((x+dx, y+dy), None) 
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
            )
            values = [v for v in values if v is not None]
            if len(values) != 2: continue
            total2 += functools.reduce(lambda a, b: int(a) * int(b), values, 1)

    return total, total2


def parse_input(filename):
    input = open(filename, 'r').read().strip().split('\n')
    data = {}
    for x in range(len(input)):
        row = input[x]
        for y in range(len(row)):
            data[x + 1j*y] = row[y]
    return data

data_test = parse_input('input-sample.txt')
result = solve(data_test)
print("Test Result: {}".format(result))

# data = open('input.txt', 'r').read().strip().split('\n')
# result = solve(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
