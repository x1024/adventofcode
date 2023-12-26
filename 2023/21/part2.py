import collections
import numpy
import pprint
import re
import functools
import itertools

neighbors = lambda x: ( x + 1, x - 1, x + 1j, x - 1j )


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
    map[start] = '.'
    data = map

    maxx = int(max(data.keys(), key=lambda x: x.real).real) + 1
    maxy = int(max(data.keys(), key=lambda x: x.imag).imag) + 1
    cells = [
        (sum(1 for x in data if data[x] == '.' and int(x.real + x.imag) % 2 == 0)),
        (sum(1 for x in data if data[x] == '.' and int(x.real + x.imag) % 2 == 1)),
    ]
    # print(start, maxx, maxy, cells)
    # exit()

    x = 0
    dist = maxx
    done = set()
    done2 = set()
    limit = 0

    @functools.lru_cache(maxsize=None)
    def bfs(start, limit):
        # print(start, limit)
        s = (0, start)
        maxx = int(max(data.keys(), key=lambda x: x.real).real) + 1
        maxy = int(max(data.keys(), key=lambda x: x.imag).imag) + 1
        queue = collections.deque([s])
        seen = set([s])
        # dist = {}
        # dist[start] = 0
        maxsteps = 0
        while queue:
            steps, now = queue.popleft()
            if steps > maxsteps:
                maxsteps = steps
                # if steps % 100 == 0: print(maxsteps)
            # if steps % 2 == limit % 2: print(steps, now)
            if steps == limit: continue
            for x2 in neighbors(now):
                # print(maxx, maxy)
                # x2_lim = x2.real % maxx + (x2.imag % maxy) * 1j
                # x2_lim = x2
                # if data[x2_lim] == '#': continue
                if data.get(x2, '#') == '#': continue

                s2 = ((steps + 1) % 2, x2)
                if s2 not in seen:
                    # dist[x2] = steps + 1
                    queue.append((steps + 1, x2))
                    seen.add(s2)
        # print(seen)
        l = [1 for a,s in seen if a % 2 == limit % 2]
        # return (len(l), maxsteps, dist)
        return (len(l), maxsteps)

    # a, maxsteps = bfs(start, l, map)
    # print(a, maxsteps)
    total = 0
    while True:
        steps_to_reach = limit * dist
        # print(limit, limit * dist + dist, l, dist)
        has_more = False
        # print(limit)

        # can reach the entirety of the rightmost cell
        print(limit)
        res = 0
        if limit == 0:
            steps_remaining = l
            v = bfs(start, steps_remaining)[0]
            # print("\t center", start, v)
            res += v
        if limit >= 1:
            steps_remaining = l - (dist // 2 + 1) - (limit - 1) * dist
            # print("\t straights", limit, steps_remaining)
            if steps_remaining >= 0:
                places = (
                    (0 + start.imag * 1j),
                    ((maxx - 1) + start.imag * 1j),
                    (start.real + 0j),
                    (start.real + (maxy - 1) * 1j),
                )
                for s2 in places:
                    st = min(steps_remaining, maxx * 2 + steps_remaining % 2)
                    v = bfs(s2, st)[0]
                    # print("\t\t", s2, v)
                    res += v 
        if limit >= 2:
            steps_remaining = l - (dist // 2 + 1) - (dist // 2 + 1) - (limit - 2) * dist
            # print("\t diagonals", limit, steps_remaining)
            if steps_remaining >= 0:
                places = (
                    (0 + 0j),
                    ((maxx - 1) + 0j),
                    (0 + (maxy - 1) * 1j),
                    ((maxx - 1) + (maxy - 1) * 1j),
                )

                for s2 in places:
                    st = min(steps_remaining, maxx * 2 + steps_remaining % 2)
                    v = bfs(s2, st)[0] * (limit - 1)
                    # print("\t\t", s2, v)
                    res += v

        if res == 0: break
        total += res
        limit += 1
        continue
            
    return (total)


dt = '''
...
.S.
...
'''[1:]
# print(main(dt, 9))
# exit()

a = '''
         ...   
         .Z.   
         Z.Z   
      ..Z.Y.Z..
      .Z.Y.Y.Z.
      Z.Y.X.Y.Z
   ..Z.Y.X.X.Y.Z..
   .Z.Y.X.O.X.Y.Z.
   Z.Y.X.O.O.X.Y.Z
..Z.Y.X.O.B.O.X.Y.Z..
.Z.Y.X.O.B_B.O.X.Y.Z.
..Z.Y.X.O.B.O.X.Y.Z..
   Z.Y.X.O.O.X.Y.Z
   .Z.Y.X.O.X.Y.Z.
   ..Z.Y.X.X.Y.Z..
      Z.Y.X.Y.Z
      .Z.Y.Y.Z.
      ..Z.Y.Z..
         Z.Z   
         .Z.   
         ...       '''

b = '''
         ...   
         .Z.   
         Z.Z   
      ..Z___Z..
      .Z.___.Z.
      Z.Y___Y.Z
   ..Z___|||___Z..
   .Z.___|||___.Z.
   Z.Y___|||___Y.Z
..Z___|||___|||___Z..
.Z.___|||___|||___.Z.
..Z___|||___|||___Z..
   Z.Y___|||___Y.Z
   .Z.___|||___.Z.
   ..Z___|||___Z..
      Z.Y___Y.Z
      .Z.___.Z.
      ..Z___Z..
         Z.Z   
         .Z.   
         ...   
'''
# for x in [1,3,5,7,9]: print(main(dt, x))

# 
dt = '''
.....
...#.
..S..
.#.#.
.....'''[1:]

dt2 = '''
..... ..Y.. .....
...#. .Y.#. ...#.
..... Y.X.Y .....
.#.#Y .#.#. Y#.#.
...Y. X.O.X .Y...

..Y.X .O.O. X.Y..
.Y.#. O.B#O .X.#.
Y.X.O .BSB. O.X.Y
.#.#. O#B#O .#.#.
..Y.X .O.O. X.Y..

...Y. X.O.X .Y...
...#Y .X.#. Y..#.
..... Y.X.Y .....
.#.#. .#.#. .#.#.
..... ..Y.. .....
'''

# print(sum(1 for x in dt2 if x in "B"))
# print(sum(1 for x in dt2 if x in "BO"))
# print(sum(1 for x in dt2 if x in "BOX"))
# print(sum(1 for x in dt2 if x in "BOXY"))
# print(sum(1 for x in dt2 if x in "BOXYZ"))
# print("-----")
# for x in [1,3,5,7,9]: print(main(dt, x))
# exit()

# exit()
# data_test = open('input-sample.txt', 'r').read().strip()
# print(main(data_test, 6))

data = open('input.txt', 'r').read().strip()
# result = main(data, 26501365)
result = main(data, 26501365)
print("Real Result: {}".format(result))
# exit()

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
