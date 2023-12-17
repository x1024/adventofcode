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
        # print(x, len(left[0]), len(right[0]), width)
        if left == right:
            yield x


def summarize(pattern):
    pattern = '\n'.join([''.join(row) for row in pattern])
    r = list(solve(pattern))
    pat2 = [list(row) for row in pattern.split("\n")]
    pat2 = np.rot90(np.array(pat2), 1)
    pat2 = '\n'.join([''.join(row) for row in pat2])
    r += [p * 100 for p in solve(pat2)]
    # print((list(solve(pattern))), (list(solve(pat2))))
    return r

def main(data):
    data = [row.strip() for row in data.split('\n\n')]
    # data = [row.split() for row in data]
    # data = list(map(int, data))
    # pprint.pprint(data)

    # part1 = sum(summarize(pattern) for pattern in data)

    result = 0
    for i, pattern in enumerate(data):
        pattern = np.array([list(row) for row in pattern.split("\n")])
        old = summarize(pattern)
        # print(old)
        done = False
        for k in range(len(pattern)):
            if done: break
            for j in range(len(pattern[0])):
                prev = pattern[k][j]
                if prev == '#':
                    pattern[k][j] = '.'
                else:
                    pattern[k][j] = '#'
                pattern_changed = ('\n'.join(''.join(row) for row in pattern))
                new = list(summarize(pattern))
                # print(k, j, new, old, prev, pattern[k][j])
                pattern[k][j] = prev

                new_line = [l for l in new if l not in old]
                if new_line:
                    result += new_line[0]
                    # print('done', new_line[0], new, old, k, j)
                    # print('\n'.join(''.join(row) for row in pattern))
                    # print()
                    # print(pattern_changed)
                    # print()
                    # print('done', new_line[0], new, old, k, j)
                    done = True
                    break

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
