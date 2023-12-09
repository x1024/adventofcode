import collections
import numpy
import pprint
import re
import functools
import itertools
import math


def get_next(nums):
    diffs = [nums[i] - nums[i-1] for i in range(1, len(nums))]
    # print(diffs)
    if len(set(diffs)) == 1 and diffs[0] == 0:
        return nums[-1]
    else:
        res = get_next(diffs)
        return res + nums[-1]

    return 0

def main(data):
    # pprint.pprint(data)
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    result = 0
    for row in data:
        n = list(map(int, row.split()))[::-1]
        print(n, get_next(n))
        result += get_next(n)


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
