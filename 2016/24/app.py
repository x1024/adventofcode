#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import queue

TILE_EMPTY = 0
TILE_WALL = 1

def tile(c):
    if c == '#': return TILE_WALL
    else: return TILE_EMPTY


def parse_input(data):
    data = [row.strip('\n') for row in data.strip('\n').split('\n')]
    # print data
    # print len(data)
    start = (0, 0)
    checkpoints = []
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if '0' == data[i][j]:
                start = (i, j)
            if '1' <= data[i][j] <= '9':
                checkpoints.append((i, j))
    room = [map(tile, row) for row in data]
    return start, checkpoints, room


def solve(data, hard_mode=False):
    start, checkpoints, room = parse_input(data)
    offsets = [ (-1,+0), (+1,+0), (+0,-1), (+0,+1), ]
    q = queue.Queue()
    key = (start, tuple(checkpoints))
    q.put(key)
    seen = {}
    seen[key] = 0

    while not q.empty():
        key = q.get()
        pos, checkpoints = key
        steps = seen[key]
        # print steps, key
        if not checkpoints:
            if not hard_mode:
                return steps
            if pos == start:
                return steps

        for offset in offsets:
            new_pos = (pos[0] + offset[0], pos[1] + offset[1])
            if room[new_pos[0]][new_pos[1]] == TILE_WALL: continue
            new_checkpoints = tuple(c for c in checkpoints if c != new_pos)
            key = (new_pos, new_checkpoints)
            if key in seen: continue
            seen[key] = steps + 1
            q.put(key)

    return -1


def easy(data):
    return solve(data)


def hard(data):
    return solve(data, hard_mode=True)


def test():
    data = '''
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
'''
    assert easy(data) == 14
    assert hard(data) == 20


if __name__ == '__main__':
    test()
    # data = sys.stdin.read()
    data = open('in.txt', 'r').read()
    print easy(data)
    print hard(data)