import collections
import numpy
import pprint
import re
import functools
import itertools
import queue

'''
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
'''

neighbors = {
    '|': ((1, 0), (-1, 0)),
    '-': ((0, 1), (0, -1)),
    'L': ((0, 1), (-1, 0)),
    'J': ((0, -1), (-1, 0)),
    '7': ((0, -1), (1, 0)),
    'F': ((0, 1), (1, 0)),
    '.': tuple(),
    'S': ((0, 1), (0, -1), (1, 0), (-1, 0)),
    'O': tuple(),
}


def get_neighbors(current, data):
    x, y = current
    for neighbor in neighbors[data[x][y]]:
        yield (x + neighbor[0], y + neighbor[1])


def bfs(start, data):
    q = queue.Queue()
    q.put((start, 0))
    visited = {}
    loop = 0

    while not q.empty():
        pos, dist = q.get()
        if pos in visited:
            if visited[pos] == dist:
                print('loop', loop, dist)
                loop = max(loop, dist)
            continue
        # print("?", pos[1], pos[0], data[pos[1]][pos[0]])
        if data[pos[0]][pos[1]] == '.':  # empty
            # print("EMPTY", pos[1], pos[0])
            continue
        visited[pos] = dist
        # print()
        # print("!", pos[0], pos[1], data[pos[0]][pos[1]])
        for neighbor in get_neighbors(pos, data):
            # print("n", neighbor)
            q.put((neighbor, dist + 1))
    return loop


def find_loop(now, start, data):
    prev = start
    loop = 1
    print("find", now, start, data[now[0]][now[1]])
    if data[now[0]][now[1]] == '.': return 0
    while True:
        if data[now[0]][now[1]] == 'S': return loop
        # data[now[0]] = data[now[0]][:now[1]] + 'O' + data[now[0]][now[1]+1:]
        # data[now[0]][now[1]] = 'O'
        for neighbor in get_neighbors(now, data):
            if neighbor == prev:
                continue
            if data[neighbor[0]][neighbor[1]] == '.':
                continue
            print(now, neighbor, data[neighbor[0]][neighbor[1]], loop)
            prev = now
            now = neighbor
            loop += 1
            break


def main(data):
    # pprint.pprint(data)
    data = data.split('\n')
    # data = list(map(int, data))
    data = ['.' + row + '.' for row in data]
    data = [(len(data[0])) * '.'] + data + [(len(data[0])) * '.']
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == 'S':
                start = (i, j)
    
    print(start)
    print("\n".join(data))
    # data[start[0]][start[1]] = '.'
    # loop = bfs(start, data)
    loop = 0
    for neighbor in get_neighbors(start, data):
        loop = max(find_loop(neighbor, start, data), loop)
    return loop // 2


data_test = '''-L|F7
7S-7|
L|7||
-L-J|
L|-JF'''
data_test = '''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''
data_test = open('input-sample.txt', 'r').read().strip()

result = main(data_test)
print("Test Result: {}".format(result))

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
