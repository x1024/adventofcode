import collections
import numpy
import pprint
import re
import functools
import itertools
import queue

transform = {
    '|': ' X  X  X ',
    '-': '   XXX   ',
    'L': ' X  XX   ',
    'J': ' X XX    ',
    '7': '   XX  X ',
    'F': '    XX X ',
    '.': '    .    ',
    'S': '    S    ',
}

offsets = [
    (0 + 1j),
    (0 + -1j),
    (1 + 0j),
    (-1 + 0j),
]


def find_loop(start):
    now = start
    last = start
    seen = set()
    loop = 0

    while True:
        seen.add(now)
        for o in offsets:
            pos = now + o
            if pos == last: continue
            c = data[pos] 
            if c == 'S': return (loop + 1) // 6, seen
            if c != 'X': continue

            last = now
            now = pos
            loop += 1
            break
        else:
            return 0, seen


data = open('input.txt', 'r').read().strip()
data = [row for row in data.split('\n')]
data = [list(row) for row in data]

data2 = {}
for i, row in enumerate(data):
    for j, pattern in enumerate(row):
        # j is from 0 to 8
        for k, c in enumerate(transform[pattern]):
            coord = (i*3 + k // 3) + (j*3 + k % 3) * 1j
            data2[coord] = c
        if data[i][j] == 'S':
            start = (i*3 + 1) + (j*3 + 1) * 1j
data = data2

loop = 0
tiles = [
    ['   ',
     ' SX',
     ' X ',],
    ['   ',
     'XS ',
     ' X ',],
    [' X ',
     'XS ',
     '   ',],
    [' X ',
     ' SX',
     '   ',],
]

seen = set()
for tile in tiles:
    for x in range(-1, 2):
        for y in range(-1, 2):
            data[start + x + y*1j] = tile[x + 1][y + 1]

    new_loop, _seen = find_loop(start)
    if new_loop > 0:
        loop = new_loop
        seen = _seen

data = dict(
        [(c, '.' if c.real % 3 == 1 and c.imag % 3 == 1 else ' ')
             for c, val in data.items()]
        + [(c, 'X') for c in seen])

max_pos = (max(c.real for c in data) + max(c.imag for c in data) * 1j)

visited = {}
def bfs(start):
    q = queue.Queue()
    q.put(start)
    size = 0

    while not q.empty():
        pos = q.get()
        if pos in visited: continue
        if not (0 <= pos.real <= max_pos.real and 0 <= pos.imag <= max_pos.imag): return 0
        if data[pos] == 'X': continue
        size += data[pos] == '.'
        visited[pos] = True
        for o in offsets: q.put(pos + o)

    return size

cells_inside = sum(
    bfs(coord) for coord in data if data[coord] == '.'
)

print(loop)
print(cells_inside)
