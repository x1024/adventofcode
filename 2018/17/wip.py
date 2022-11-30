import pprint
import collections
import numpy
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(100000)


EMPTY = ' '
WALL = '#'
WATER = '|'
STILL_WATER = '~'
START_X = 500
START_Y = 0
BLOCKED = 1
DONE = 2

def solve(_input):
  board = collections.defaultdict(lambda: EMPTY)
  min_y = 9999999
  max_y = START_Y
  min_x = START_X
  max_x = START_X
  for row in _input:
    xs = row['x']
    ys = row['y']
    for x in range(xs[0], xs[-1]+1):
      min_x = min(x, min_x - 0)
      max_x = max(x, max_x + 2)
      for y in range(ys[0], ys[-1]+1):
        board[(x, y)] = WALL
        min_y = min(y, min_y)
        max_y = max(y, max_y)
  # print(max_y, min_x, max_x)

  def propagate(pos):
    if board[pos] == WATER: return DONE
    if board[pos] != EMPTY: return BLOCKED
    if pos[0] < min_x or pos[0] > max_x: return DONE
    if pos[1] > max_y: return DONE
    board[pos] = WATER
    down = (pos[0], pos[1] + 1)
    if board[down] == EMPTY:
      res = propagate(down)
      if res == DONE: return DONE

    if board[down] == WALL or board[down] == STILL_WATER:
      left = (pos[0] - 1, pos[1])
      right = (pos[0] + 1, pos[1])
      res = []
      if board[left] == EMPTY:
        res.append(propagate(left))
      if board[right] == EMPTY:
        res.append(propagate(right))
      x, y = pos
      __min_x = x
      wall_left = False
      while x >= min_x:
        if board[(x, y)] == WALL:
          wall_left = True
          __min_x = x + 1
          break
        if board[(x, y)] != WATER:
          break
        x -= 1
      
      x, y = pos
      __max_x = x
      wall_right = False
      while x >= min_x:
        if board[(x, y)] == WALL:
          __max_x = x - 1
          wall_right = True
          break
        if board[(x, y)] != WATER:
          break
        x += 1
      if wall_left and wall_right:
        for x in range(__min_x, __max_x + 1):
          board[(x, y)] = STILL_WATER
      if DONE in res: return DONE

    pass

  # pprint.pprint(input)
  propagate((START_X, START_Y))
  # print_board(board, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)
  still_water = sum(1 for (x, y), val in board.items() if val in [STILL_WATER] and x >= min_x and y >= min_y and x <= max_x and y <= max_y)
  water = sum(1 for (x, y), val in board.items() if val in [WATER] and x >= min_x and y >= min_y and x <= max_x and y <= max_y)
  total_water = water + still_water
  # Don't count the start position
  return still_water
  return total_water


def print_board(board, min_x=490, max_x=510, min_y=0, max_y=20):
  for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
      print(board[(x, y)], end="")
    print('  %s' % y)


def parse_line(input):
  parts = input.split(', ')
  data = {}
  for part in parts:
    coordinate = part[0]
    pixels = part[2:]
    values = list(map(int, pixels.split('..')))
    data[coordinate] = values
  return data

def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  print(result)
  assert result == 29
  exit()
  return


# test()

_input = open('input.txt', 'r').read().strip()
_input = parse_input(_input)
result = solve(_input)
print("Result: {}".format(result))
