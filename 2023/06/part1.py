import collections
import numpy
import pprint
import re
import functools
import itertools


def main(data):
    # pprint.pprint(data)
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    result = 0
    print(data)
    time = list(map(int, data[0].split()[1:]))
    distance = list(map(int, data[1].split()[1:]))
    print(time, distance)

    result = 1
    data = zip(time, distance)
    for row in data:
        # print(row)
        t, d = row
        wins = 0
        for i in range(t):
            rest = t - i
            total_dist = rest * i
            print(row, i, rest, total_dist, d, total_dist >= d)
            if total_dist > d:
                wins += 1
        result *= wins
        print(row, wins, result)
    

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
