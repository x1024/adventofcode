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
HALLWAY = -1 * TILE
BAD_HALLWAY = -1 * (TILE + 1)
CHARACTER = -10


def get_crab(crab):
    c, pos = crab
    return (ord(c) - ord('A'), pos)

def parse_input(data):
    data = [row.strip() for row in data.strip("\n").split("\n")]
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
    # print crabs
    assert len(crabs) == 8
    return crabs

def normalize_state(crabs):
    return tuple(
        sorted(crabs[0:2]) +
        sorted(crabs[2:4]) +
        sorted(crabs[4:6]) +
        sorted(crabs[6:8])
    )

bad_hallways = (
    (1, 3),
    (1, 5),
    (1, 7),
    (1, 9),
)

offsets = [
    (0,  1),
    (0, -1),
    ( 1, 0),
    (-1, 0),
]

costs = [1, 1, 10, 10, 100, 100, 1000, 1000]
crab_types = [
    CRAB_A, CRAB_A,
    CRAB_B, CRAB_B,
    CRAB_C, CRAB_C,
    CRAB_D, CRAB_D,
]

def parse_row(row):
    return map(lambda c: TILE if c == '#' else EMPTY, row)
    
maze_template_str = '''
#############
#...........#
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
        print ''.join(r)


def get_maze(crabs):
    maze = [row[::] for row in maze_template]
    # print_maze(maze)
    x, y = crabs[0]
    maze[x][y] = CRAB_A
    x, y = crabs[1]
    maze[x][y] = CRAB_A

    x, y = crabs[2]
    maze[x][y] = CRAB_B
    x, y = crabs[3]
    maze[x][y] = CRAB_B

    x, y = crabs[4]
    maze[x][y] = CRAB_C
    x, y = crabs[5]
    maze[x][y] = CRAB_C

    x, y = crabs[6]
    maze[x][y] = CRAB_D
    x, y = crabs[7]
    maze[x][y] = CRAB_D
    return maze


def move_crab(crab, maze):
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
                yield (new_moves, new_pos)
                q.put((new_moves, new_pos))
                seen.add(new_pos)

  
def get_moves(crabs):
    maze = get_maze(crabs)
    # print_maze(maze)
    # raw_input()
    # The crabs always go AA BB CC DD
    # print 'get maze'
    # print_maze(maze)
    # raw_input()
    # print "---"
    crabs = list(crabs)
    for i, crab in enumerate(crabs):
        x, y = crab
        crab_type = maze[x][y]
        start_type = maze_template[x][y]
        maze[x][y] = start_type
        cost = costs[i]
        # print_maze(maze)
        # raw_input()
        # print i, 'moves:'
        for moves, pos in move_crab(crab, maze):
            x1, y1 = pos
            destination = maze[x1][y1]
            if start_type == HALLWAY and destination != -1 * crab_type:
                # the crab can *only* go back to its place
                continue
            if destination == BAD_HALLWAY:
                continue
            if DESTINATION_D <= destination <= DESTINATION_A:
                if destination != -1 * crab_type:
                    # another crab type's home
                    continue
                bottom_cell = maze[x1][y1+1]
                is_valid = (bottom_cell == TILE or
                            bottom_cell == crab_type)
                if not is_valid:
                    # There's another crab in our home
                    continue

            maze[x1][y1] = CHARACTER
            new_cost = cost * moves
            # print "crab: %s, destination: %s, cost: %s, pos: %s" % (
            #     i, destination, new_cost, pos, 
            # )
            # print_maze(maze)
            # raw_input()

            # move is good, send it
            old_crab_pos = crabs[i]
            crabs[i] = pos
            yield new_cost, normalize_state(crabs)
            crabs[i] = old_crab_pos
            maze[x1][y1] = destination

        # Restore the initial state of the maze
        maze[x][y] = crab_type
        # print "---"


def solve(data, end_state, debug):
    initial_state = parse_input(data)
    q = queue.PriorityQueue()
    q.put((0, initial_state))
    seen = {}
    max_cost = 0
    # seen[initial_state] = (0, False)

    if debug:
        debug = map(parse_input, debug)
    
    while not q.empty():
        state = q.get()
        cost, crabs = state

        if crabs in seen: continue
        seen[crabs] = cost

        if debug and crabs in debug:
            print "Cost: %s, state: %s" % (cost, crabs)
            print_maze(get_maze(crabs))
            print crabs
            print end_state
        if not debug and cost > max_cost + 50:
            print "Cost: %s, state: %s" % (cost, crabs)
            print_maze(get_maze(crabs))
            max_cost = cost

        if crabs == end_state:
            print "END:"
            print "--------"
            print "Cost: %s, state: %s" % (cost, end_state)
            print_maze(get_maze(end_state))
            return cost

        for move_cost, new_crabs in get_moves(crabs):
            new_cost = cost + move_cost
            # print new_crabs

            q.put((new_cost, new_crabs))
            # seen[new_crabs] = (new_cost, crabs)
            # seen.add(new_crabs)
    result = 0
    return result


def easy(data, end_state = None, debug=None):
    if not end_state:
        end_state = '''
            #############
            #...........#
            ###A#B#C#D###
            ###A#B#C#D###
            #############
        '''
    # print end_state
    end_state = parse_input(end_state)

    return solve(data, end_state, debug=debug)


def hard(data):
    return solve(data)


def debug_state(state):
    parsed = parse_input(state)
    print state
    print parsed
    print_maze(get_maze(parsed))

def test_easy():
    states = []
    states.append((0, '''
        #############
        #...........#
        ###B#C#B#D###
        ###A#D#C#A###
        #############
    '''))

    states.append((40, '''
        #############
        #...B.......#
        ###B#C#.#D###
        ###A#D#C#A###
        #############
    '''))
    # assert easy(data, end_state) == 40

    states.append((400, '''
        #############
        #...B.......#
        ###B#.#C#D###
        ###A#D#C#A###
        #############
    '''))

    states.append((3000+30, '''
        #############
        #.....D.....#
        ###B#.#C#D###
        ###A#B#C#A###
        #############
    '''))

    states.append((40, '''
        #############
        #.....D.....#
        ###.#B#C#D###
        ###A#B#C#A###
        #############
    '''))

    states.append((2000, '''
        #############
        #.....D.D...#
        ###.#B#C#.###
        ###A#B#C#A###
        #############
    '''))

    states.append((3, '''
        #############
        #.....D.D.A.#
        ###.#B#C#.###
        ###A#B#C#.###
        #############
    '''))
    states.append((3000, '''
        #############
        #.....D...A.#
        ###.#B#C#.###
        ###A#B#C#D###
        #############
    '''))
    states.append((4000, '''
        #############
        #.........A.#
        ###.#B#C#D###
        ###A#B#C#D###
        #############
    '''))

    states.append((8, '''
        #############
        #...........#
        ###A#B#C#D###
        ###A#B#C#D###
        #############
    '''))

    print states[-2][1]
    # assert easy(states[-2][1]) == 8
    # assert easy(states[-3][1]) == 7008
    # print easy(states[1][1])

    # states = states[5:]
    debug = [state for cost, state in states]
    total_cost = sum(cost for cost, state in states[1:])
    for c in debug: print c
    print total_cost
    value = easy(states[0][1], debug=debug)
    print total_cost
    print value
    assert value == total_cost

    # for i in range(len(states)-1):
    #     _, state = states[i]
    #     cost, end_state = states[i+1]
    #     print '----'
    #     print cost, state
    #     assert easy(state, end_state) == cost
    # for i in range(len(states)-1):
    #     for j in range(i + 1, len(states)):
    #         total_cost = sum(cost for cost, state in states[i:j+1])
    #         state = states[i][1]
    #         end_state = states[j][1]
    #         print '-----'
    #         print i, j
    #         print total_cost
    #         print state
    #         print '-'
    #         print end_state
    #         assert easy(state, end_state) == total_cost
def test_hard():
    states = open('in_hard_test.txt', 'r').read().split('\n\n')
    new_states = []
    for state in states:
        state = state.split('\n')
        state = '\n'.join(row.replace(' ', '#').ljust(len(state[0]), '#')
            for row in state)
        new_states.append(state)
    states = new_states

    for state in states:
        print state
        print '---'


def test():
    # test_easy()
    test_hard()
    exit()


def main():
    test()
    test_hard()
    # exit()
    # data = open('in.txt').read()
    data = '''
#############
#...........#
###B#A#A#D###
###B#C#D#C###
#############
'''
    print easy(data)
    # print hard(data)


if __name__ == '__main__':
    main()