import pprint
import collections
import numpy


WALL = 'X'
LUMBER = '#'
TREE = '|'
OPEN = '.'

def iterate(board):
  d = [-1, 0, 1]
  '''
 • An open acre will become filled with trees if three or more adjacent acres
   contained trees. Otherwise, nothing happens.
 • An acre filled with trees will become a lumberyard if three or more adjacent
   acres were lumberyards. Otherwise, nothing happens.
 • An acre containing a lumberyard will remain a lumberyard if it was adjacent
   to at least one other lumberyard and at least one acre containing trees.
   Otherwise, it becomes open.
  '''
  def neighbours(y, x):
    res = collections.defaultdict(lambda: 0)
    for dy in d:
      for dx in d:
        b = board[y+dy][x+dx]
        res[b] += 1
    res[board[y][x]] -= 1
    return res

  board2 = [row.copy() for row in board]
  ROWS = len(board) - 2
  for y in range(1, ROWS + 1):
    for x in range(1, ROWS + 1):
      n = neighbours(y, x)
      b = board[y][x]
      if b == OPEN:
        if n[TREE] >= 3:
          b = TREE
      elif b == TREE:
        if n[LUMBER] >= 3:
          b = LUMBER
      elif b == LUMBER:
        if not (n[LUMBER] >= 1 and n[TREE] >= 1):
          b = OPEN
      board2[y][x] = b
  return board2

def solve(input, iterations=1000000000):
  seen = {}
  ROWS = len(input)
  board = []
  board.append([WALL] * (ROWS + 2))
  for _ in range(ROWS):
    board.append(list(WALL + ''.join([OPEN] * ROWS) + WALL))
  board.append([WALL] * (ROWS + 2))

  for y in range(ROWS):
    for x in range(ROWS):
      v = input[y][x]
      board[y+1][x+1] = v
  print('\n'.join(''.join(row) for row in board))
  looped = False
  i = 0
  while i < iterations:
    i += 1
    board = iterate(board)
    state = '\n'.join(''.join(row) for row in board)
    print(i, len(seen), iterations)
    if state in seen and not looped:
      looped = True
      loop = i - seen[state]
      print(i, seen[state], loop)
      # print(state)
      iterations = (iterations - i) % loop + i
      print(i, seen[state], loop, iterations)
    seen[state] = i
    # print('\n'.join(''.join(row) for row in board))
  c = collections.Counter(''.join(''.join(row) for row in board))
  # print(c)
  return c[LUMBER] * c[TREE]


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  return input


def test():
  input = '''
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
'''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  assert result == 1147
  exit()


# test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
