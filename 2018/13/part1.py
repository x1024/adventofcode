import pprint
import collections
import numpy

HORIZONTAL = '-'
VERTICAL = '|'
INTERSECTION = '+'
ANGLE_RIGHT = '/'
ANGLE_LEFT = '\\'
EMPTY = ' '

DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

STATE_LEFT = 0
STATE_FORWARD = 1
STATE_RIGHT = 2
OFFSETS = { 
  DIR_LEFT: (0, -1),
  DIR_DOWN: (1, 0),
  DIR_RIGHT: (0, 1),
  DIR_UP: (-1, 0),
 }

def solve(data, carts):
  def step(carts):
    result = []
    for (x, y, dir, state) in carts:
      dx, dy = OFFSETS[dir]
      pos = (x + dx, y + dy)
      tile = data[pos]
      if tile == INTERSECTION:
        if state == STATE_LEFT:
          dir = (dir - 1 + 4) % 4
          state = STATE_FORWARD
        elif state == STATE_FORWARD:
          state = STATE_RIGHT
        elif state == STATE_RIGHT:
          dir = (dir + 1) % 4
          state = STATE_LEFT
      elif tile == ANGLE_RIGHT: # /
        if dir == DIR_UP: dir = DIR_RIGHT
        elif dir == DIR_DOWN: dir = DIR_LEFT
        elif dir == DIR_LEFT: dir = DIR_DOWN
        elif dir == DIR_RIGHT: dir = DIR_UP
      elif tile == ANGLE_LEFT: # \
        if dir == DIR_UP: dir = DIR_LEFT
        elif dir == DIR_DOWN: dir = DIR_RIGHT
        elif dir == DIR_LEFT: dir = DIR_UP
        elif dir == DIR_RIGHT: dir = DIR_DOWN
      result.append((pos[0], pos[1], dir, state))
    return result

  i = 0
  while True:
    i += 1
    carts = step(carts)
    print(i, carts)
    crash = detect_crash(carts)
    if crash:
      # print(crash)
      return crash[::-1]
    # print_state(data, carts)

  return 0


def detect_crash(carts):
  for x in range(len(carts)):
    for y in range(x + 1, len(carts)):
      p1 = carts[x][:2]
      p2 = carts[y][:2]
      # print(x, y, p1, p2)
      if p1 == p2:
        return p1
  return False



def print_state(data, carts):
  d = {}
  for x, y, dir, state in carts:
    d[x,y] = dir

  for x in range(6):
    for y in range(13):
      if (x,y) in d:
        dir = d[x,y]
        if dir == DIR_UP: dir = '^'
        elif dir == DIR_DOWN: dir = 'v'
        elif dir == DIR_RIGHT: dir = '>'
        elif dir == DIR_LEFT: dir = '<'
        print(dir, end='')
      else:
        print(data[x,y], end='')
    print('')

def parse_line(input):
  return input.split()

def parse_input(input):
  input = input.split('\n')
  # input = [row.strip() for row in input]
  input = [row for row in input if row]
  data = {}
  carts = []
  for x, row in enumerate(input):
    for y, cell in enumerate(row):
      # print (x, y, cell)
      if cell == '>': carts.append((x, y, DIR_RIGHT, STATE_LEFT))
      if cell == '<': carts.append((x, y, DIR_LEFT, STATE_LEFT))
      if cell == 'v': carts.append((x, y, DIR_DOWN, STATE_LEFT))
      if cell == '^': carts.append((x, y, DIR_UP, STATE_LEFT))

      if cell in ['|', 'v', '^']:
        c = VERTICAL
      elif cell in ['-', '>', '<']:
        c = HORIZONTAL
      elif cell == '+':
        c = INTERSECTION
      elif cell == '\\':
        c = ANGLE_LEFT
      elif cell == '/':
        c = ANGLE_RIGHT
      else:
        c = EMPTY
      data[x,y] = c

  for x, row in enumerate(input):
    print(len(row), row)
  return data, carts


def test():
  input = '''
/->-\         
|   |  /----\ 
| /-+--+-\  | 
| | |  | v  | 
\-+-/  \-+--/ 
  \------/    '''
  data, carts = parse_input(input)
  result = solve(data, carts)
  print("Test Result: {}".format(result))
  return


test()
# exit()
input = open('input.txt', 'r').read().strip()
data, carts = parse_input(input)
result = solve(data, carts)
print("Result: {}".format(result))
