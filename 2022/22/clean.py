import IPython
import re

# data = open('input.txt', 'r').read()
from data_test import SIDE_WIDTH, data, neighbors, offsets
from data import SIDE_WIDTH, data, neighbors, offsets

chars = '>v<^'
def mark_board(board, pos, dir):
  board[pos[0]][pos[1]] = chars[dir]

def print_board(board, pos, dir):
  mark_board(board, pos, dir)
  return
  for row in board: print(''.join(row))
  print()
  # input()
  # board[pos[0]][pos[1]] = old

# data = [row.strip() for row in data]
# data = list(map(int, data))
# data = [row.split() for row in data]

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
dirs = [
  (0, 1), # right
  (1, 0), # bottom
  (0, -1),
  (-1, 0),
]

def rotate_clockwise(state):
  x, y, direction = state
  direction = (direction + 1) % len(dirs)
  x, y = y, SIDE_WIDTH - 1 - x
  # print('rotate clockwise', state, (x, y, direction))
  return x, y, direction

S = SIDE_WIDTH


def move(data, path):
  def get_board(sx, sy):
    board = []
    for x in range(sx * S, (sx + 1) * S):
      row = []
      for y in range((sy * S), (sy + 1) * S):
        row.append(data[x][y])
      board.append(row)
    return board

  boards = [None] + [get_board(x, y) for (x, y) in offsets.values()]

  pos = (0, 0)
  current_board = 1
  # path = path[:5]
  dir = RIGHT
  offset = offsets[current_board]
  global_pos = (pos[0] + offset[0] * S, pos[1] + offset[1] * S)
  print(current_board, pos, global_pos, offset)
  print_board(data, global_pos, dir)

  print("initial dir", dir)
  for (steps, turn) in path:
    print("New move", steps, turn)
    offset = offsets[current_board]
    global_pos = (pos[0] + offset[0] * S, pos[1] + offset[1] * S)
    print_board(data, global_pos, dir)
    for i in range(steps):
      # board = boards[current_board]
      forward = dirs[dir]
      new_pos = (pos[0] + forward[0]), (pos[1] + forward[1])
      print("moving", i, steps, pos, dir, forward, new_pos)
      to_move = None
      if new_pos[0] >= SIDE_WIDTH: to_move = DOWN
      if new_pos[0] < 0: to_move = UP
      if new_pos[1] >= SIDE_WIDTH: to_move = RIGHT
      if new_pos[1] < 0: to_move = LEFT

      if to_move is not None:
        neighbor = neighbors[current_board][to_move]
        new_board_index, transform = neighbor
        print("switch board", to_move, new_board_index)
        # print(pos, dir)
        # nx = max(0, min(SIDE_WIDTH - 1, new_pos[0]))
        # ny = max(0, min(SIDE_WIDTH - 1, new_pos[1]))
        # new_pos = nx, ny
        x, y, new_dir = transform((new_pos[0], new_pos[1], dir))
        x = (x + SIDE_WIDTH) % SIDE_WIDTH
        y = (y + SIDE_WIDTH) % SIDE_WIDTH
        new_pos = (x, y)
        print("new board pos/dir", new_pos, new_dir)
        # print(pos, new_dir)
      else:
        print("not switching board", new_pos, dir)
        new_board_index = current_board
        new_pos = new_pos
        new_dir = dir

      new_board = boards[new_board_index]
      if new_board[new_pos[0]][new_pos[1]] == '#':
        print("WALL")
        # it's a wall
        continue
      else:
        pos = new_pos
        current_board = new_board_index
        dir = new_dir

      offset = offsets[current_board]
      global_pos = (pos[0] + offset[0] * S, pos[1] + offset[1] * S)
      print("move done", pos, dir, global_pos)
      # print_board(data, global_pos, dir)
      mark_board(data, global_pos, dir)

    if turn == 'R':
      dir = (dir + 1) % len(dirs)
    elif turn == 'L':
      dir = (dir - 1 + len(dirs)) % len(dirs)

    offset = offsets[current_board]
    global_pos = (pos[0] + offset[0] * S, pos[1] + offset[1] * S)
    print("------------")
    print_board(data, global_pos, dir)
    print("------------")
    # print(steps, turn)
  print(pos, dir)
  print("------------")
  print("------------")
  print("------------")
  offset = offsets[current_board]
  global_pos = (pos[0] + offset[0] * S, pos[1] + offset[1] * S)
  print_board(data, global_pos, dir)
  pos = global_pos
  print(pos)
  print("------------")
  return 1000 * (pos[0] + 1) + (pos[1] + 1) * 4 + dir


data = data.replace("_", " ")
data = data.split('\n')
path = data[-1]
data = data[:-2]
data = [[c for c in row] for row in data if row]
path = re.findall("\d+[R|L|N]", path + "N")
path = [(int(c[:-1]), c[-1]) for c in path]
# print(path)
print(move(data, path))
exit()
# 6032
# 5031

print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
