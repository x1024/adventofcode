import re

data = open('input.txt', 'r').read()

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

# from data import DATA, OFFSETS, NEIGHBORS, SIDE_WIDTH
from data_test import DATA, OFFSETS, NEIGHBORS, SIDE_WIDTH

S = SIDE_WIDTH

DIRECTIONS = { 
  RIGHT: (0, 1), # right
  DOWN: (1, 0), # bottom
  LEFT: (0, -1),
  UP: (-1, 0),
}


def rotate_clockwise(pos):
  x, y = pos
  x, y = y, SIDE_WIDTH - 1 - x
  return (x, y)


def global_pos(state):
  pos, current_board, dir = state
  offset = OFFSETS[current_board]
  return (pos[0] + offset[0] * SIDE_WIDTH, pos[1] + offset[1] * SIDE_WIDTH)


def mark_board(board, state):
  pos = global_pos(state)
  dir = state[2]
  board[pos[0]][pos[1]] = '>v<^'[dir]



def move_forward(boards, state):
  '''
  Moves one step forward, unless obstructed by wall.
  Switches to another "board" if moving past the edge of the current one.
  '''

  pos, current_board, direction = state
  forward = DIRECTIONS[direction]
  new_pos = (pos[0] + forward[0]), (pos[1] + forward[1])

  to_move = None
  if new_pos[0] >= SIDE_WIDTH: to_move = DOWN
  elif new_pos[0] < 0: to_move = UP
  elif new_pos[1] >= SIDE_WIDTH: to_move = RIGHT
  elif new_pos[1] < 0: to_move = LEFT

  if to_move is not None:
    neighbor = NEIGHBORS[current_board][to_move]
    new_board_index, rotations = neighbor
    # print("switch board", to_move, new_board_index)
    new_dir = (direction + rotations) % len(DIRECTIONS)
    while rotations > 0:
      new_pos = rotate_clockwise(new_pos)
      rotations -= 1
    new_pos = (new_pos[0] % SIDE_WIDTH, new_pos[1] % SIDE_WIDTH)
    # print("new board pos/dir", new_pos, new_dir)
  else:
    # print("not switching board", new_pos, direction)
    new_pos = new_pos
    new_board_index = current_board
    new_dir = direction

  new_board = boards[new_board_index]
  if new_board[new_pos[0]][new_pos[1]] != '#':
    pos = new_pos
    current_board = new_board_index
    direction = new_dir

  return (pos, current_board, direction)


def make_turn(state, turn):
  (pos, current_board, direction) = state
  if turn == 'R': direction = (direction + 1) % len(DIRECTIONS)
  elif turn == 'L': direction = (direction - 1) % len(DIRECTIONS)
  return (pos, current_board, direction)


def get_board(data, sx, sy):
  '''Returns once "side" of the 6-sided dice, as a square grid'''
  return [data[x][(sy*S):(sy + 1)*S] for x in range(sx*S, (sx + 1)*S)]


def walk_path(data, path):
  boards = [get_board(data, x, y) for (x, y) in OFFSETS]
  # print("\n".join(''.join(row) for row in data))

  pos = (0, 0)
  current_board = 1 # Boards are indexes 1-6 (for now)
  direction = RIGHT
  state = (pos, current_board, direction)

  for (steps, turn) in path:
    for _ in range(steps):
      state = move_forward(boards, state)
      mark_board(data, state)
    state = make_turn(state, turn)

  direction = state[2]
  pos = global_pos(state)
  return 1000 * (pos[0] + 1) + (pos[1] + 1) * 4 + direction


data, path = DATA.replace("_", " ").split("\n\n")
data = list(map(list, data.split('\n')))
path = [(int(c[:-1]), c[-1]) for c in re.findall("\d+[R|L|N]", path + "N")]
result = walk_path(data, path)
print(result)