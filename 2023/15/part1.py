import collections
import numpy
import pprint
import re
import functools
import itertools

def hash(string):
    current = 0
    for s in string:
        current += ord(s)
        current *= 17
        current %= 256
    return current


def main(data):
    # pprint.pprint(data)
    print(data)
    return sum([hash(p) for p in data.split(',')])
    print(parts)
    exit()
    # data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    # parse into a grid
    # for r, row in enumerate(data):
    #     for c, col in enumerate(row):
    #         coord = (c + r * 1j)
    #         map[coord] = col

    result = 0




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