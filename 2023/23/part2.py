import collections
import time
import numpy
import pprint
import re
import functools
import itertools
import sys
sys.setrecursionlimit(100000)


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
    for delta in deltas['.']:
        neighbor = pos + delta
        if neighbor in map and map[ neighbor ] != '#':
            neighbors.append(delta)
    return neighbors


def is_crossroads(map, pos):
    return len(get_neighbors(map, pos)) > 2

opposites = dict((
       (1, '_'),
       (-1, '_'),
       (1j, '_'),
       (-1j, '_'),
))

def dfs(map, start, end):
    queue = [start]
    answers = []
    def _dfs():
        pos = queue[-1]
        # print(pos, len(queue), queue)
        if pos == end:
            answers.append(len(queue) - 1)
            print(max(answers), len(answers))
            # exit()
            return

        for offset in get_neighbors(map, pos):
            next_pos = pos + offset
            # print("\t", next_pos)
            if next_pos in queue: continue
            queue.append(next_pos)
            _dfs()
            queue.pop()

    _dfs()
    return answers
    # return res


def main(data):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    # parse into a grid
    map = collections.defaultdict(lambda: '#')
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            coord = (c + r * 1j)
            map[coord] = col

    start = 1
    maxx = max(map.keys(), key=lambda x: x.real).real
    maxy = max(map.keys(), key=lambda x: x.imag).imag * 1j
    end = (maxx - 1 + maxy)
    # print(map)

    q = collections.deque()
    q.append((start, 0, {start: -1 -1j}))
    res = dfs(map, start, end)
    print(res)
    print(max(res))
    return 
    done = {}
    done[start] = 0
    res = 0
    while q:
        pos, dist, seen = q.popleft()
        print(pos, dist, seen)
        for pos, dist, seen in bfs(map, pos, end, seen, dist):
            if done.get(pos, 0) >= dist:
                continue
            done[pos] = dist
            if pos == end:
                res = max(res, dist)
            q.append((pos, dist, seen))

    return res


data_test = open('input-sample.txt', 'r').read().strip()
data_test2 = '''
#.#######
#v#######
#.>.>...#
#v#v###v#
#.>.>.>.#
#######.#
'''[1:]
# data_test = data_test2
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
