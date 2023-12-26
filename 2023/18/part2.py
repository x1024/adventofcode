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
            print(i)
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
    lines = []
    vert = []
    horz = []
    horz2 = []
    for row in data:
        dir, n, color = row.split()
        dir = dirmap[color[7]]
        n = int(color[2:2+5], 16)
        start = pos
        end = pos + directions[dir] * int(n)
        pos = end

        # print(color, n, dir, start, end)
        if start.real > end.real or start.imag > end.imag:
            tmp = start
            start = end
            end = tmp

        if dir in 'UD':
            assert(start.real == end.real)
            vert.append((start, end))
        else:
            assert(start.imag == end.imag)
            horz.append(start.imag)
            horz2.append((start, end))

    vert = list(sorted(set(vert), key=lambda v: v[0].real))
    horz = list(sorted(set(horz)))
    # horz2 = list(sorted(set(horz2)))
    # print(horz)
    # pprint.pprint(vert)
    # pprint.pprint(horz2)

    # res -= len(data)

    volume = 0
    # print(horz)
    print(min(horz), max(horz))
    for x in range(int(min(horz)), int(max(horz)) + 1):
        verts = [v[0].real for v in vert if v[0].imag < x and v[1].imag >= x]
        horzs = [(h[0].real, h[1].real) for h in horz2 if h[0].imag <= x and h[0].imag >= x]
        horzs = sorted(horzs)
        verts = sorted(verts)
        height = 1
        slices = horzs
        for i in range(0, len(verts) - 1, 2):
            slices.append((verts[i], verts[i+1]))
        slices = list(sorted(slices))
        row = 0
        now = slices[0][0]
        for s in slices:
            # print("\t", now, s, s[1] - max(s[0], now) + 1)
            row += max(0, s[1] - max(s[0], now) + 1)
            now = max(s[1] + 1, now)
        # print(x, row, slices)
        volume += row

    return (volume)

    exit()
    volume += sum([v[2] - v[1] + 1 for v in horz2])
    volume -= len(data)

    return volume
    # return volume
    # pprint.pprint(vert)
    # pprint.pprint(horz)
    # exit()

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


# data_test = open('input-sample.txt', 'r').read().strip()
# # result = main(data_test)
# print("Test Result: {}".format(result))

# exit()

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
