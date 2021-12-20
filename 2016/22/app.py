#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import queue

INDEX_X = 0
INDEX_Y = 1
INDEX_SIZE = 2
INDEX_USED = 3
INDEX_AVAILABLE = 4


def parse_line(line):
    x, y = [int(cell[1:]) for cell in line[0].split('-')[1:]]
    size, used, available, used_percentage = [int(cell.strip('T%')) for cell in line[1:]]
    return (x, y, size, used, available)


def parse_input(data):
    data = [row.split() for row in data.split('\n')[2:]]
    return map(parse_line, data)


def easy(data):
    def check(i, j):
        if i == j: return False
        return data[i][INDEX_USED] > 0 and data[i][INDEX_USED] <= data[j][INDEX_AVAILABLE]
    data = parse_input(data)
    return sum(check(i, j)
        for i in range(len(data))
        for j in range(len(data)))


def hard(data):
    data = parse_input(data)
    def find(pos):
        return [d for d in data if d[:2] == pos][0]

    max_pos = max(row[0] for row in data), max(row[1] for row in data)
    start_cell = find((0, 0))
    goal_cell = find((max_pos[0], 0))
    free_cell = [cell for cell in data if cell[INDEX_AVAILABLE] > goal_cell[INDEX_USED]][0]

    used = [[0] * (max_pos[1] + 1) for _ in range(max_pos[0] + 1)]
    sizes = [[0] * (max_pos[1] + 1) for _ in range(max_pos[0] + 1)]
    for cell in data:
        x, y = cell[:2]
        sizes[x][y] = cell[INDEX_SIZE]
        used[x][y] = cell[INDEX_USED]
    used = tuple(map(tuple, used))
    sizes = tuple(map(tuple, sizes))

    offsets = ( (+1, +0), (-1, +0), (+0, -1), (+0, +1))

    def is_inside(cell):
        if cell[0] < 0 or cell[1] < 0: return False
        if cell[0] > max_pos[0] or cell[1] > max_pos[1]: return False
        return True

    def get_neighbours(cell, used):
        x, y = cell
        free_space = sizes[x][y] - used[x][y]
        neighbours = [(x + dx, y + dy) for (dx, dy) in offsets]
        # print neighbours
        neighbours = [n for n in neighbours if is_inside(n)]
        # print neighbours
        neighbours = [n for n in neighbours if used[n[0]][n[1]] <= free_space]
        # print neighbours
        # raw_input()
        return neighbours

    start = start_cell[:2]
    goal = goal_cell[:2]
    free = free_cell[:2]

    q = queue.Queue()
    seen = {}
    start_state = (free, goal, used)

    def print_state(state):
        free, goal, _ = state
        for y in range(max_pos[1] + 1):
            for x in range(max_pos[0] + 1):
                pos = (x, y)
                if pos == free: c = '_'
                elif pos == goal: c = 'G'
                else: c = '.'
                c = "%c%03d" % (c, used[x][y])
                # print cells[pos][INDEX_SIZE],
                print c,
            print

    max_steps = 0
    q.put(start_state)
    seen[(free, goal)] = (0, None)
    while not q.empty():
        state = q.get()
        (free, goal, used) = state
        key = (free, goal)
        steps, _ = seen[key]
        if steps > max_steps:
            max_steps = steps
            print >>sys.stderr, steps, q.qsize()

        if goal == start:
            # steps, prev_state = seen[state[:2]]
            # states = [state]
            # while prev_state:
            #     states.append(prev_state)
            #     prev_state = seen[prev_state[:2]][1]
            # states = states[::-1]
            # print '---'
            # for state in states:
            #     print_state(state)
            #     print
            #     raw_input()
            # print steps
            return steps

        def generate_used(used, free, new_free):
            used = list(map(list, used))
            x,y = free
            nx, ny = new_free
            used[x][y] += used[nx][ny]
            used[nx][ny] = 0
            used = tuple(map(tuple, used))
            return used

        for new_free in get_neighbours(free, used):
            new_free = new_free[:2]
            new_goal = free if new_free == goal else goal
            new_used = generate_used(used, free, new_free)

            new_state = (new_free, new_goal, new_used)
            key = (new_free, new_goal)
            if key in seen: continue
            seen[key] = (steps + 1, state)
            q.put(new_state)


def test():
    data = '''root@ebhq-gridcenter# df -h
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%'''
    assert hard(data) == 7


def main():
    import sys
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()