import pprint
import collections
import numpy
import IPython

EMPTY = 0
WALL = 1
SAND = 2

EMPTY = '.'
WALL = '#'
SAND = 'o'

def print_data(data, sand):
  for y in range(0, 20):
    for x in range(490, 510):
      cell = data[x, y]
      if (x,y) == sand: cell = SAND
      print(cell, end="")
    print()

def solve(input):
  data = collections.defaultdict(lambda: EMPTY)
  max_y = 0
  for row in input:
    x, y = row[0]
    max_y = max(y, max_y)
    for nx, ny in row[1:]:
      # print('!', x, y, nx, ny)
      max_y = max(ny, max_y)
      if x == nx:
        for _y in range(min(y, ny), max(y, ny) + 1):
          # print(nx, _y)
          data[(nx, _y)] = WALL
      else:
        for _x in range(min(x, nx), max(x, nx) + 1):
          data[(_x, ny)] = WALL
          # print(_x, ny)
      x, y = nx, ny
  # print_data(data)
  # print(max_y)
  start = (500, 0)
  sand = 0
  while True:
    x, y = start
    while True:
      print(x, y, data[x, y], data[x, y+1])
      # print_data(data, (x,y))
      if y > max_y:
        print("DONE")
        return (sand)
      if data[(x, y+1)] == EMPTY:
        y = y + 1
      elif data[(x-1, y+1)] == EMPTY:
        x = x - 1
        y = y + 1
      elif data[(x+1, y+1)] == EMPTY:
        x = x + 1
        y = y + 1
      else:
        data[(x, y)] = SAND
        sand += 1
        break
    print(sand)
    if y > max_y:
      print("DONE")
      return (sand)


def parse_line(input):
  input = input.split(" -> ")
  input = [tuple(map(int, row.split(","))) for row in input]
  return input


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
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

IPython.embed()
