import re

data = open('input.txt', 'r').read()

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

from data import DATA, OFFSETS, NEIGHBORS, SIDE_WIDTH
# from data_test import DATA, OFFSETS, NEIGHBORS, SIDE_WIDTH

S = SIDE_WIDTH

DIRECTIONS = { 
  RIGHT: (0, 1),
  DOWN: (1, 0),
  LEFT: (0, -1),
  UP: (-1, 0),
}


def rotate_clockwise(pos):
  x, y = pos
  x, y = y, SIDE_WIDTH - 1 - x
  return (x, y)


def step_forward(state, boards):
  '''
  Moves one step forward, unless obstructed by wall.
  Switches to another "board" if moving past the edge of the current one.
  '''

  pos, current_board, direction = state
  forward = DIRECTIONS[direction]
  pos = (pos[0] + forward[0]), (pos[1] + forward[1])

  if pos[0] >= SIDE_WIDTH: to_move = DOWN
  elif pos[0] < 0: to_move = UP
  elif pos[1] >= SIDE_WIDTH: to_move = RIGHT
  elif pos[1] < 0: to_move = LEFT
  else: to_move = None

  if to_move is not None:
    # print("switch board", to_move, current_board)
    neighbor = NEIGHBORS[current_board][to_move]
    current_board, rotations = neighbor
    direction = (direction + rotations) % len(DIRECTIONS)
    [pos := rotate_clockwise(pos) for i in range(rotations)]
    pos = (pos[0] % SIDE_WIDTH, pos[1] % SIDE_WIDTH)

  if boards[current_board][pos[0]][pos[1]] != '#':
    return (pos, current_board, direction)
  return state


def make_turn(state, turn):
  (pos, current_board, direction) = state
  if turn == 'R': direction = (direction + 1) % len(DIRECTIONS)
  elif turn == 'L': direction = (direction - 1) % len(DIRECTIONS)
  return (pos, current_board, direction)


def get_board(data, sx, sy):
  '''Returns one "side" of the 6-sided dice, as a square grid'''
  return [data[x][(sy*S):(sy + 1)*S] for x in range(sx*S, (sx + 1)*S)]


def walk_path(data, path):
  boards = [get_board(data, x, y) for (x, y) in OFFSETS]
  state = ((0, 0), 1, RIGHT) # Boards are indexes 1-6 (for now)

  for (steps, turn) in path:
    [state := step_forward(state, boards) for _ in range(steps)]
    state = make_turn(state, turn)

  # Get the global position from the local one
  pos, current_board, direction = state
  offset = OFFSETS[current_board]
  pos = (pos[0] + offset[0] * SIDE_WIDTH, pos[1] + offset[1] * SIDE_WIDTH)
  return 1000 * (pos[0] + 1) + (pos[1] + 1) * 4 + direction


data, path = DATA.replace("_", " ").split("\n\n")
data = list(map(list, data.split('\n')))
path = [(int(c[:-1]), c[-1]) for c in re.findall("\d+[R|L|N]", path + "N")]
result = walk_path(data, path)
print(result)