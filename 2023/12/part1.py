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

def main(data):
    # pprint.pprint(data)
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))
    result = 0
    # data = data[1:2]
    print(data)

    for row in data:
        found = 0
        spring, expected = row.split(' ')
        expected = list(map(int, expected.split(',')))
        options = list(solve(spring))
        # print('!', spring, len(options))
        for option in options:
            # option = re.sub(r'\.+', '.', option)
            # print(option)
            pieces = [len(r) for r in option.split('.') if len(r) > 0]
            # print(option, expected, pieces)
            if pieces == expected:
                found += 1
        # print('found', row, expected, found)
        result += found

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
