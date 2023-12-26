
import collections
import numpy
import pprint
import re
import functools
import itertools

directions = {
    'U': -1j,
    'R': 1,
    'D': 1j,
    'L': -1,
}

def bfs(start, map):
    q = collections.deque()
    q.append((start, 0))
    seen = set()
    i = 0
    while q:
        i += 1
        if i % 100000 == 0:
            print(i, len(seen))
        pos, dist = q.popleft()
        if pos in seen:
            continue
        seen.add(pos)
        map[pos] = 1
        for dir in directions.values():
            new_pos = pos + dir
            if new_pos in map:
                continue
            q.append((new_pos, dist + 1))
    return None

dirmap = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U',
}

def main(data):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))
    pos = 0 + 0j
    map = {}
    for row in data:
        dir, n, color = row.split()
        dir = dirmap[color[7]]
        n = int(color[2:2+5], 16)
        print(color, n, dir)
        for x in range(int(n)):
            pos += directions[dir]
            map[pos] = 1

    for y in range(10):
        for x in range(10):
            coord = x + y * 1j
            if coord in map:
                print(map[coord], end='')
            else:
                print(' ', end='')
        print()
    print(sum(map.values()))
    bfs(1 + 1j, map)
    for y in range(10):
        for x in range(10):
            coord = x + y * 1j
            if coord in map:
                print(map[coord], end='')
            else:
                print(' ', end='')
        print()
    print(sum(map.values()))

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

exit()

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
