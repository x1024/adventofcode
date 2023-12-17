import collections
import numpy as np
import pprint
import re
import functools
import itertools

def solve(pattern):
    # print(pattern)
    pattern = pattern.split('\n')
    result = 0
    l = len(pattern[0])
    for x in range(1, l):
        width = min(x, l - x)
        left = [row[x-width:x] for row in pattern]
        right = [row[x:x+width][::-1] for row in pattern]
        print(x, len(left[0]), len(right[0]), width)
        if left == right:
            yield x
    yield 0


def main(data):
    data = [row.strip() for row in data.split('\n\n')]
    # data = [row.split() for row in data]
    # data = list(map(int, data))
    # pprint.pprint(data)

    result = 0
    for i, pattern in enumerate(data):
        r = sum(solve(pattern))
        pat2 = [list(row) for row in pattern.split("\n")]
        pat2 = np.rot90(np.array(pat2), 1)
        pat2 = '\n'.join([''.join(row) for row in pat2])
        r += sum(solve(pat2)) * 100
        print((list(solve(pattern))), (list(solve(pat2))))
        result += r
    return result


# data_test = open('input-sample.txt', 'r').read().strip()
# result = main(data_test)
# print("Test Result: {}".format(result))

# exit()

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
