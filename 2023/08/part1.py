import collections
import numpy
import pprint
import re
import functools
import itertools


def main(data):
    # pprint.pprint(data)
    instructions, data = data.split('\n\n')
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = list(map(int, data))
    print(instructions)

    result = 0

    r = {}
    for row in data:
        f, to = row.split(" = ")
        to = to.replace('(', '').replace(')', '').split(', ')
        r[f] = to

    print(r)
    start = 'AAA'
    end = 'ZZZ'

    now = 'AAA'
    print(now)
    i = 0
    while True:
        c = instructions[i % len(instructions)]
        now = r[now][0 if c == 'L' else 1]
        i += 1
        if now == end:
            return i

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
