import collections
import time
import numpy
import pprint
import re
import functools
import itertools

deltas = {
    '.': (1, -1, 1j, -1j),
    'v': (1j,),
    '>': (1,),
    '<': (-1,),
    '^': (-1j,),
    '#': tuple(),
}

def get_neighbors(map, pos):
    neighbors = []
    for delta in deltas[ map[ pos ] ]:
        neighbor = pos + delta
        if neighbor in map and map[ neighbor ] != '#':
            neighbors.append(delta)
    return neighbors


def is_crossroads(map, pos):
    return len(get_neighbors(map, pos)) > 2

opposites = dict((
       (1, '<'),
       (-1, '>'),
       (1j, '^'),
       (-1j, 'v'),
))

def bfs(map, start, end, dist=0):
    queue = collections.deque()
    queue.append((start, dist))
    seen = set()
    while queue:
        pos, dist = queue.popleft()
        print(map[pos], pos, dist)
        # time.sleep(1)
        if pos != start and is_crossroads(map, pos):
            yield pos, dist
            continue

        if pos == end:
            yield pos, dist
            continue
        if pos in seen: continue
        seen.add(pos)
        for offset in get_neighbors(map, pos):
            next_pos = pos + offset
            print("\t", offset, opposites[offset], pos, next_pos, map[next_pos])
            if map[next_pos] == '#': continue
            if map[next_pos] == opposites[offset]: continue
            queue.append((next_pos, dist + 1))
    # return res


def main(data):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    # parse into a grid
    seen = {}
    map = collections.defaultdict(lambda: '#')
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            seen[col] = seen.get(col, 0) + 1
            coord = (c + r * 1j)
            map[coord] = col

    start = 1
    maxx = max(map.keys(), key=lambda x: x.real).real
    maxy = max(map.keys(), key=lambda x: x.imag).imag * 1j
    end = (maxx - 1 + maxy)
    # print(map)

    q = collections.deque()
    q.append((start, 0))
    done = {}
    done[start] = 0
    res = 0
    while q:
        pos, dist = q.popleft()
        print('map', pos, dist)
        for pos, dist in bfs(map, pos, end, dist):
            print(pos, dist)
            if done.get(pos, 0) >= dist:
                continue
            done[pos] = dist
            if pos == end:
                res = max(res, dist)
            q.append((pos, dist))
        print("-----")
        print(len(q))

    return res


data_test = open('input-sample.txt', 'r').read().strip()
data_test2 = '''
#.####
#v####
#.>..#
#v##v#
#.>..#
####.#
'''[1:]
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
