#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import queue

EMPTY = 0
CRAB_A = 1
CRAB_B = 2
CRAB_C = 3
CRAB_D = 4
TILE = 5
DESTINATION_A = -1 * CRAB_A
DESTINATION_B = -1 * CRAB_B
DESTINATION_C = -1 * CRAB_C
DESTINATION_D = -1 * CRAB_D
BAD_HALLWAY = -1 * TILE
CHARACTER = -10

bad_hallways = ( (1, 3), (1, 5), (1, 7), (1, 9),)

offsets = [ (0,  1), (0, -1), ( 1, 0), (-1, 0), ]

# costs = [1, 1, 10, 10, 100, 100, 1000, 1000]
costs = [1, 1, 1, 1, 10, 10, 10, 10, 100, 100, 100, 100, 1000, 1000, 1000, 1000]


def parse_input(data):
    data = [row.strip() for row in data.strip("\n").split("\n")]
    data = ['##' + row + '##' if len(row) == 9 else row
        for row in data]
    data = [row for row in data if row]
    crabs = [
        [],
        [],
        [],
        [],
    ]
    for i in range(len(data)):
        for j in range(len(data[0])):
            c = data[i][j]
            if c == 'A': crabs[0].append((i, j))
            if c == 'B': crabs[1].append((i, j))
            if c == 'C': crabs[2].append((i, j))
            if c == 'D': crabs[3].append((i, j))

    crabs = crabs[0] + crabs[1] + crabs[2] + crabs[3]
    crabs = normalize_state(crabs)
    # assert len(crabs) == 8
    assert len(crabs) == 16
    return crabs

def normalize_state(crabs):
    step = len(crabs) / 4
    return tuple(
        sorted(crabs[0:step]) +
        sorted(crabs[step:step*2]) +
        sorted(crabs[step*2:step*3]) +
        sorted(crabs[step*3:step*4])
    )


def parse_row(row):
    return map(lambda c: TILE if c == '#' else EMPTY, row)
    
maze_template_str = '''
#############
#...........#
###.#.#.#.###
###.#.#.#.###
###.#.#.#.###
###.#.#.#.###
#############
'''.strip('\n')
maze_template = [parse_row(row)
    for row in maze_template_str.split('\n')]
for h in bad_hallways:
    maze_template[h[0]][h[1]] = BAD_HALLWAY

for i in range(2, len(maze_template)-1):
    maze_template[i][3] = DESTINATION_A
    maze_template[i][5] = DESTINATION_B
    maze_template[i][7] = DESTINATION_C
    maze_template[i][9] = DESTINATION_D


# for row in maze_template: print row
def print_maze(maze):
    for row in maze:
        r = []
        for c in row:
            if c == TILE: r.append('#')
            elif c == CRAB_A: r.append('A')
            elif c == CRAB_B: r.append('B')
            elif c == CRAB_C: r.append('C')
            elif c == CRAB_D: r.append('D')
            elif c == CHARACTER: r.append('@')
            else: r.append('.')
        print >>sys.stderr, ''.join(r)


def get_maze(crabs):
    maze = [row[::] for row in maze_template]
    # print_maze(maze)
    l = len(crabs) / 4
    for i in range(l*0, l*1):
        x, y = crabs[i]
        maze[x][y] = CRAB_A
    for i in range(l*1, l*2):
        x, y = crabs[i]
        maze[x][y] = CRAB_B
    for i in range(l*2, l*3):
        x, y = crabs[i]
        maze[x][y] = CRAB_C
    for i in range(l*3, l*4):
        x, y = crabs[i]
        maze[x][y] = CRAB_D
    return maze


def hash_maze(maze):
    maze = [map(lambda c: '.' if c <= EMPTY else '#', row) for row in maze]
    maze = [''.join(row) for row in maze]
    maze = '\n'.join(maze)
    return maze

def hash_crabs(crabs):
    result = 0
    for crab in crabs:
        result = result * 15 * 15 + crab[0] * 15 + crab[1]
    return result

memo = {}
def move_crab(crab, maze):
    key = (crab, hash_maze(maze))
    cached = memo.get(key, None)
    if cached is not None:
        return cached

    all_moves = []
    q = queue.PriorityQueue()
    seen = set()
    seen.add(crab)
    q.put((0, crab))

    while not q.empty():
        moves, pos = q.get()
        for offset in offsets:
            x, y = (pos[0] + offset[0], pos[1] + offset[1])
            if maze[x][y] <= EMPTY:
                new_pos = (x, y)
                new_moves = moves + 1
                if new_pos in seen: continue
                new_move = (new_moves, new_pos)
                all_moves.append(new_move)
                q.put((new_moves, new_pos))
                seen.add(new_pos)
    memo[key] = all_moves
    return all_moves


def crab_should_stay(crab, crab_type, maze):
    x, y = crab
    if crab_type == maze[x][y] * -1:
        # This crab is already in its home
        for i in range(x + 1, len(maze) - 1):
            if maze[i][y] != crab_type:
                # There are other crabs below this one
                # so it needs to leave, then come back
                return False
        return True
    return False

  
def get_moves(crabs):
    maze = get_maze(crabs)
    crabs = list(crabs)
    for i, crab in enumerate(crabs):
        x, y = crab
        crab_type = maze[x][y]
        start_type = maze_template[x][y]
        maze[x][y] = start_type
        cost = costs[i]

        if crab_should_stay(crab, crab_type, maze):
            continue

        for moves, pos in move_crab(crab, maze):
            x1, y1 = pos
            destination = maze[x1][y1]
            bottom_cell = maze[x1+1][y1]

            if start_type == destination:
                # There are actually no optimal moves
                # that cause a crab to go to the same type of tile it started on
                continue

            if not (bottom_cell == TILE or bottom_cell == crab_type):
                # The crab never needs to *not* be at the bottom of a home.
                # This is because it can only ever enter its own home,
                # and every home needs to be filled
                continue

            if not (destination == -1 * crab_type or destination == EMPTY):
                # The crab always ends up either in a hallway or in its own home
                continue

            if destination == -1 * crab_type:
                # No crabs of other types can be present in the home
                cells = (maze[c][y1] for c in range(x + 1, len(maze) - 1))
                if any(CRAB_A < maze[c][y1] <= CRAB_D and maze[c][y1] != crab_type
                    for c in cells):
                    continue

            maze[x1][y1] = CHARACTER
            new_cost = cost * moves

            # move is good, send it
            old_crab_pos = crabs[i]
            crabs[i] = pos
            yield new_cost, normalize_state(crabs)
            crabs[i] = old_crab_pos
            maze[x1][y1] = destination

        # Restore the initial state of the maze
        maze[x][y] = crab_type


def print_path(crabs, previous):
    path = []
    while crabs:
        path.append(crabs)
        crabs = previous[crabs]
    for step in path[::-1]:
        print_maze(get_maze(step))
        print >>sys.stderr, "-----"
        raw_input()


def get_heuristic(crabs):
    step = len(crabs) / 4
    # goals = ( (9, 2), (9, 3), (9, 4), (9, 5))
    # lowest crab first
    d_crabs = list(reversed(sorted(crabs[step*3:step*4])))
    goals = ((5, 9), (4, 9), (3, 9), (2, 9))
    result = 0
    for i in range(4):
        c = d_crabs[i]
        g = goals[i]
        if c[1] != 9:
            # Crab has to move up to row 1 first
            result += 1000 * abs(c[0] - 1)
            c = (1, c[1])
        result += 1000 * (abs(c[0] - g[0]) + abs(c[1] - g[1]))
    return result


def solve(data):
    end_state = parse_input('''
        #############
        #...........#
        ###A#B#C#D###
        ###A#B#C#D###
        ###A#B#C#D###
        ###A#B#C#D###
        #############
    ''')
    initial_state = parse_input(data)

    seen = set()
    previous = {}
    q = queue.PriorityQueue()
    q.put((0, 0, initial_state, None))
    max_cost = 0

    while not q.empty():
        state = q.get()
        _, cost, crabs, previous_crabs = state

        hashed = hash_crabs(crabs)
        if hashed in seen: continue
        seen.add(hashed)
        previous[crabs] = previous_crabs

        if cost > max_cost + 1000:
            print >>sys.stderr, "Cost: %s, seen: %s" % (cost, len(seen))
            print_maze(get_maze(crabs))
            max_cost = cost

        if crabs == end_state:
            # print_path(crabs, previous)
            return cost

        for move_cost, new_crabs in get_moves(crabs):
            new_cost = cost + move_cost
            heuristic = get_heuristic(new_crabs)
            q.put((new_cost + heuristic, new_cost, new_crabs, crabs))

    result = 0
    return result


def easy(data):
    extra_rows = [
        '  #A#B#C#D#  ',
        '  #A#B#C#D#  ',
    ]
    data = data.split('\n')
    data = data[:4] + extra_rows + data[4:]
    data = '\n'.join(data)
    return solve(data)


def hard(data):
    extra_rows = [
        '  #D#C#B#A#  ',
        '  #D#B#A#C#  ',
    ]
    data = data.split('\n')
    data = data[:3] + extra_rows + data[3:]
    data = '\n'.join(data)
    return solve(data)


def parse_states(filename):
    return open(filename, 'r').read().split('\n\n')


def test_easy():
    states = parse_states('in_easy_test.txt')
    assert easy(states[0]) == 12521


def test_hard():
    states = parse_states('in_hard_test.txt')
    assert hard(states[0]) == 44169


def test():
    test_easy()
    test_hard()


def main():
    test()
    data = parse_states('in.txt')[0]
    print easy(data)
    print hard(data)

if __name__ == '__main__':
    main()