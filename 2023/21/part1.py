import collections
import numpy
import pprint
import re
import functools
import itertools

neighbors = lambda x: [x + 1, x - 1, x + 1j, x - 1j]

def bfs(start, limit, data):
    s = (0, start)
    queue = collections.deque([s])
    seen = set([s])
    while queue:
        steps, now = queue.popleft()
        print(steps, now)
        if steps == limit: continue
        for x2 in neighbors(now):
            if data.get(x2, '#') == '#':
                continue

            state = ((steps + 1) % 2, x2)
            if state not in seen:
                queue.append((steps + 1, x2))
                seen.add(state)
    print(seen)
    l = [s for s in seen if s[0] == limit % 2]
    print(l)
    return (len(l))

def main(data, l):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    # parse into a grid
    map = {}
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            coord = (c + r * 1j)
            map[coord] = col

    # print(map)
    start = (x for x in map if map[x] == 'S').__next__()
    print(start)
    return bfs(start, l, map)

    result = 0




    print(result)
    return result


data_test = open('input-sample.txt', 'r').read().strip()
result = main(data_test, 6)
print("Test Result: {}".format(result))

# exit()

data = open('input.txt', 'r').read().strip()
result = main(data, 64)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
