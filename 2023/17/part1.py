import collections
import numpy
import pprint
import re
import functools
import itertools
import queue

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

opposite = {
    UP: DOWN,
    RIGHT: LEFT,
    DOWN: UP,
    LEFT: RIGHT,
}
directions = {
    UP: -1j,
    RIGHT: 1,
    DOWN: 1j,
    LEFT: -1,
}

def bfs(start, end, map):
    q = queue.PriorityQueue()
    q.put((0, (start.real, start.imag, 0, 0)))
    # seen = set()
    seen = {}
    seen2 = {}
    i = 0

    while not q.empty():
        dist, pos = q.get()
        i += 1
        if i % 100000 == 0:
            print(i, pos, dist, seen2.get(end, 999999999999))
        c1, c2, direction, steps = pos
        coord = c1 + c2 * 1j
        # print(pos, dist)

        if seen.get(pos, 999999999999) <= dist:
            continue
        seen[pos] = dist
        seen2[coord] = min(seen2.get(coord, 999999999999), dist)

        # if coord == end: return seen

        for dir, offset in directions.items():
            new_pos = coord + offset
            if new_pos not in map: continue
            value = map[new_pos]
            # print(dir, offset)
            if dir == opposite[direction]: continue
            elif dir == direction:
                if steps >= 3: continue
                q.put((dist + value, (new_pos.real, new_pos.imag, dir, steps + 1)))
            else:
                q.put((dist + value, (new_pos.real, new_pos.imag, dir, 1)))

    return seen2


def main(data):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    # parse into a grid
    # map = collections.defaultdict(lambda: 0)
    map = {}
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            coord = (c + r * 1j)
            map[coord] = int(col)

    maxx, maxy = max(x.imag for x in map), max(x.real for x in map)
    end = maxx + maxy * 1j
    seen = bfs((0 + 0j), end, map)
    return (seen[end])

    # print(map)
    # print(data)
    result = 0




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
