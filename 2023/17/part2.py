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
NONE = -1

opposite = {
    UP: DOWN,
    RIGHT: LEFT,
    DOWN: UP,
    LEFT: RIGHT,
    NONE: NONE,
}
directions = {
    UP: -1j,
    RIGHT: 1,
    DOWN: 1j,
    LEFT: -1,
}

def bfs(start, end, map):
    q = queue.PriorityQueue()
    q.put((0, (start.real, start.imag, -1)))
    # seen = set()
    seen = {}
    seen2 = {}
    i = 0

    while not q.empty():
        dist, pos = q.get()
        i += 1
        if i % 100000 == 0:
            print(i, pos, dist, seen2.get(end, 999999999999))
        c1, c2, direction = pos
        coord = c1 + c2 * 1j
        # print(pos, dist)

        if seen.get(pos, 999999999999) <= dist:
            continue
        seen[pos] = dist
        seen2[coord] = min(seen2.get(coord, 999999999999), dist)

        # if coord == end: return seen

        for dir, offset in directions.items():
            if dir == opposite[direction]: continue
            if dir == direction: continue
            for steps in range(4, 10+1):
            # for steps in range(1, 3+1):
                value = 0
                for s in range(1, steps+1):
                    c = coord + offset * s
                    if c not in map: break
                    value += map[c]
                else:
                    # q.put(((new_pos, dir), dist + value))
                    new_pos = coord + offset * steps
                    q.put((dist + value, (new_pos.real, new_pos.imag, dir)))


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

    maxy, maxx = int(max(x.imag for x in map)), int(max(x.real for x in map))
    end = maxx + maxy * 1j
    print(end)
    seen = bfs((0 + 0j), end, map)
    print(maxx, maxy)
    for y in range(maxy+1):
        for x in range(maxx+1):
            print(seen.get( x + y*1j, -1), end=' ')
        print()
    return (seen[end])

    # print(map)
    # print(data)
    result = 0




    print(result)
    return result


data_test = open('input-sample.txt', 'r').read().strip()
data_test = '''111111111111
999999999991
999999999991
999999999991
999999999991'''
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
