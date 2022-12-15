import pprint
import collections
import numpy


dirs = {
  'U': (-1, 0),
  'D': (+1, 0),
  'L': (0, -1),
  'R': (0, +1),
}

def p(h, t):
  LIM = 5
  print(h, t)
  for x in range(-LIM, LIM):
    for y in range(-LIM, LIM):
      if (x, y) == h:
        print("H", end="")
      elif (x, y) == t:
        print("T", end="")
      elif (x, y) == (0, 0):
        print("s", end="")
      else:
        print(".", end="")
    print()
  print()

def solve(data):
  head = (0, 0)
  tail = (0, 0)
  p(head, tail)
  seen = set()
  for command in data:
    dir, count = command
    offset = dirs[dir]
    print(dir, offset, count)
    for i in range(count):
      head = head[0] + offset[0], head[1] + offset[1]
      dx = head[0] - tail[0]
      dy = head[1] - tail[1]
      print(abs(dx), abs(dy), abs(dx) >= 2 or abs(dy) >= 2)
      if abs(dx) >= 2 or abs(dy) >= 2:
        if dx > 0:
          dx = 1
        elif dx < 0:
          dx = -1
        else:
          dx = 0
        if dy > 0:
          dy = 1
        elif dy < 0:
          dy = -1
        else:
          dy = 0
        print(dx, dy)
        tail = tail[0] + dx, tail[1] + dy
      # p(head, tail)
      seen.add(tail)
      # input()

  return len(seen)


def parse_line(input):
  (dir, count) = input.split()
  return dir, int(count)


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

