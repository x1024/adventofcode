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
    # 'S': ((0, 1), (0, -1), (1, 0), (-1, 0)),
    'S': ((0, 1), (1, 0)),

    '0': tuple(),
    '1': tuple(),
    '2': tuple(),
    '3': tuple(),
}

transform = {
    '|': [
        ' X ',
        ' X ',
        ' X ',
    ],
    '-': [
        '   ',
        'XXX',
        '   ',
    ],
    'L': [
        ' X ',
        ' XX',
        '   ',
    ],
    'J': [
        ' X ',
        'XX ',
        '   ',
    ],
    '7': [
        '   ',
        'XX ',
        ' X ',
    ],
    'F': [
        '   ',
        ' XX',
        ' X ',
    ],
    '.': [
        '   ',
        ' . ',
        '   ',
    ],
    'S': [
        # 'ZZZ',
        # 'ZZZ',
        # 'ZZZ',
        '   ',
        ' XX',
        ' X ',
    ],
}


def get_neighbors(current, data):
    x, y = current
    for neighbor in neighbors[data[x][y]]:
        yield (x + neighbor[0], y + neighbor[1])


offsets = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]

def bfs(start, data, visited):
    q = queue.Queue()
    q.put(start)
    size = 0
    outside = False
    changed = []

    while not q.empty():
        pos = q.get()
        if pos in visited:
            continue
        if pos[0] == 0 or pos[1] == 0 or pos[0] == len(data) or pos[1] == len(data[0]):
            outside = True
            continue
        if data[pos[0]][pos[1]] == 'X':
            continue
        if data[pos[0]][pos[1]] == '.':
            changed.append(pos)
            size += 1
        visited[pos] = True

        for o in offsets:
            pos2 = (pos[0] + o[0], pos[1] + o[1])
            q.put(pos2)

    print('asd', changed, outside)
    if outside:
        for c in changed:
            data[c[0]][c[1]] = ' '
        return 0, visited
    return len(changed), visited


def find_loop(now, start, data, loop_char):
    prev = start
    loop = 1
    print("find", now, start, data[now[0]][now[1]])
    if data[now[0]][now[1]] == '.': return 0
    while True:
        if data[now[0]][now[1]] == 'S': return loop
        # data[now[0]] = data[now[0]][:now[1]] + 'O' + data[now[0]][now[1]+1:]
        # data[now[0]][now[1]] = 'O'
        neighbors = list(get_neighbors(now, data))
        if not neighbors:
            break
        data[now[0]][now[1]] = loop_char
        for neighbor in neighbors:
            if neighbor == prev:
                continue
            if data[neighbor[0]][neighbor[1]] == '.':
                continue
            print(now, neighbor, data[neighbor[0]][neighbor[1]], loop)
            prev = now
            now = neighbor
            loop += 1
            break
    return loop


def num_intersections(pos, offset, data, loop_char):
    intersections = 0
    while True:
        pos = (pos[0] + offset[0], pos[1] + offset[1])
        if pos[0] < 0 or pos[1] < 0:
            return intersections
        if pos[0] >= len(data) or pos[1] >= len(data[0]):
            return intersections
        if data[pos[0]][pos[1]] == loop_char:
            intersections += 1

def is_enclosed(pos, data, loop_char):
    x, y = pos
    intersections = [
        num_intersections(pos, (0, +1), data, loop_char),
        num_intersections(pos, (0, -1), data, loop_char),
        num_intersections(pos, (+1, 0), data, loop_char),
        num_intersections(pos, (-1, 0), data, loop_char),
    ]
    print(x, y, intersections)
    return all(i % 2 == 1 for i in intersections)
    print(intersections)



def main(data):
    # pprint.pprint(data)
    data = data.split('\n')
    # data = list(map(int, data))
    data = ['.' + row + '.' for row in data]
    data = [(len(data[0])) * '.'] + data + [(len(data[0])) * '.']
    data = [list(row) for row in data]
    data3 = [list(row) for row in data]
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == 'S':
                start = (i, j)
    
    loop = 0
    loop_char = '0'
    for i, neighbor in enumerate(get_neighbors(start, data)):
        new_loop = find_loop(neighbor, start, data, str(i))
        if new_loop > loop:
            loop = new_loop
            loop_char = str(i)
    data[start[0]][start[1]] = loop_char
    print("\n".join(''.join(row) for row in data))

    data2 = []
    for i, row in enumerate(data3):
        row2 = [transform[c if data[i][j] == '0' else '.'] for j, c in enumerate(row)]
        data2.append(list(''.join(''.join(r[0]) for r in row2)))
        data2.append(list(''.join(''.join(r[1]) for r in row2)))
        data2.append(list(''.join(''.join(r[2]) for r in row2)))

    for row in data2:
        print(''.join(row))

    visited = {}
    result = 0
    for x in range(len(data2)):
        for y in range(len(data2[0])):
            if data2[x][y] == '.':
                size, visited = bfs((x, y), data2, visited)
                result += size

    for row in data2:
        print(''.join(row))

    return loop // 2, result

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
data_test = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''
data_test = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''

data_test = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''
# data_test = open('input-sample.txt', 'r').read().strip()

# result = main(data_test)
# print("Test Result: {}".format(result))

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
