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
        print(start, limit)
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
        print(limit)

        # can reach the entirety of the rightmost cell
        if (limit + 2) * dist < l:
            parity = (limit + 1) % 2
            c = limit * 4 if limit > 0 else 1

            print("ASDASDASD", limit, dist, limit * dist, l, cells[parity] * c)
            total += cells[parity] * c
            limit += 1
        else:
            # print("Limit", limit, dist, (limit - 1) * dist + dist // 2 + 1, l)
            # print(total)

            # for x in [0, limit]:
            for x in range(0, limit + 1):
                y = limit - x
                if (x, y) in done: continue
                steps_to_reach = 0
                if x > 0:
                    steps_to_reach += dist // 2 + 1
                    steps_to_reach += (x - 1) * dist
                if y > 0:
                    steps_to_reach += dist // 2 + 1
                    steps_to_reach += (y - 1) * dist

                vals = set(( (x, y), (-x, y), (x, -y), (-x, -y), ))
                for val in vals:
                    if val in done: continue
                    done.add(val)
                    sx, sy = int(start.real), int(start.imag)
                    dx, dy = val
                    if dx > 0: sx = 0
                    if dx < 0: sx = maxx - 1
                    if dy > 0: sy = 0
                    if dy < 0: sy = maxy - 1
                    start2 = (sx + sy * 1j)
                    # if start2 in done2: continue
                    # done2.add(start2)
                    steps_remaining = l - steps_to_reach
                    if steps_remaining < 0:
                        continue
                    # print(start2, (x, y), (dx, dy), steps_to_reach, l, steps_remaining)
                    res = bfs(start2, min(maxx * 2, steps_remaining))[0]
                    has_more = True
                    # print("\t", val, steps_remaining, start2, res)
                    total += res
            # print(limit, dist, l)
            # print((limit - 1) * dist + dist // 2 + 1 + dist // 2 + 1, l)
        if not has_more: break
        limit += 1

    print(total)
    exit()
    return (total)


dt = '''
...
.S.
...
'''[1:]
print(main(dt, 7))

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
# dt = '''
# .....
# ...#.
# ..S..
# .#.#.
# .....'''[1:]
# 
# dt2 = '''
# ..... ..Y.. .....
# ...#. .Y.#. ...#.
# ..... Y.X.Y .....
# .#.#Y .#.#. Y#.#.
# ...Y. X.O.X .Y...
# 
# ..Y.X .O.O. X.Y..
# .Y.#. O.B#O .X.#.
# Y.X.O .BSB. O.X.Y
# .#.#. O#B#O .#.#.
# ..Y.X .O.O. X.Y..
# 
# ...Y. X.O.X .Y...
# ...#Y .X.#. Y..#.
# ..... Y.X.Y .....
# .#.#. .#.#. .#.#.
# ..... ..Y.. .....
# '''
# 
# print(sum(1 for x in dt2 if x in "B"))
# print(sum(1 for x in dt2 if x in "BO"))
# print(sum(1 for x in dt2 if x in "BOX"))
# print(sum(1 for x in dt2 if x in "BOXY"))
# # print(sum(1 for x in dt2 if x in "BOXYZ"))
# print("-----")
# 

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
