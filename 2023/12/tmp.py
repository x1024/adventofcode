import collections
import numpy
import pprint
import re
import functools
import itertools


def solve(spring):
    # print(spring)
    if len(spring) == 0:
        yield ''
        return

    for i in solve(spring[1:]):
        if spring[0] == '?':
            yield '#' + i
            yield '.' + i
        else:
            yield spring[0] + i


'''
.#....###....##
1 3 2
'''


@functools.lru_cache(maxsize=None)
def solve(spring, expected):
    print('asd', spring, expected)
    if not spring: return 1

    if spring[0] == '?':
        return solve('.' + spring[1:], expected) + solve('#' + spring[1:], expected)

    if spring[0] == '.':
        return solve(spring[1:], expected)

    result = 0
    if spring[0] == '#':
        if not expected:
            return 0
        remaining = expected[0] - 1
        if remaining == 0:
            return solve(spring[1:], expected[1:])
        else:
            return solve(spring[1:], (remaining, ) + expected[1:])

    return 0



def main(data):
    # pprint.pprint(data)
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))
    result = 0
    data = data[0:1]

    for row in data:
        found = 0
        spring, expected = row.split(' ')
        spring = '?'.join(spring for i in range(5))
        expected = ','.join(expected for i in range(5))
        print(spring, expected)

        expected = tuple(map(int, expected.split(',')))
        result += solve(spring, expected)

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
