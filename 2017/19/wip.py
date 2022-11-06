import os
import sys
import time

def solve(input):
  print(input)
  return 0


def parse_line(input):
  return input.split()

EMPTY = ' '
LINE = '█'
TURN = '+'

DOWN = 0
UP = 1
LEFT = 2
RIGHT = 3

OFFSETS = {
  DOWN: (1, 0),
  UP: (-1, 0),
  LEFT: (0, -1),
  RIGHT: (0, 1),
}

TURNS = {
  DOWN: [DOWN, LEFT, RIGHT],
  UP: [UP, LEFT, RIGHT],
  LEFT: [LEFT, UP, DOWN],
  RIGHT: [RIGHT, UP, DOWN],
}


def parse_input(input):
  letters = {}
  data = {}
  input = input.split('\n')
  start_pos = (0, 0)
  for i, row in enumerate(input):
    for j, col in enumerate(row):
      pos = (i, j)
      # print(i, j, col)
      if col == ' ':
        tile = EMPTY
      else:
        tile = LINE
        if col >= 'A' and col <= 'Z':
          letters[pos] = col
      if i == 0 and tile == LINE:
        start_pos = pos
      data[pos] = tile
  return start_pos, data, letters


def print_maze(data, pos):
  size = (max(data.keys()))
  print(size)
  for i in range(size[0]+1):
    for j in range(size[1]+1):
      if (i, j) == pos:
        print("X", end="")
      else:
        tile = data[(i, j)]
        print(tile, end=""),
    print()

def traverse(start, data, letters):
  dir = DOWN
  pos = start
  size = (max(data.keys()))
  message = []
  steps = 1
  while True:
    if pos[0] < 0 or pos[1] < 0 or pos[0] > size[0] or pos[1] > size[1]:
      break
    tile = data.get(pos, EMPTY)
    if pos in letters:
      message.append(letters[pos])
    if tile == LINE:
      for d in TURNS[dir]:
        o = OFFSETS[d]
        p1 = (pos[0] + o[0], pos[1] + o[1])
        if data.get(p1, EMPTY) == LINE:
          pos = p1
          dir = d
          break
      else:
        break
    else:
      break
    steps += 1
    # print(pos, ''.join(message))
    # print_maze(data, pos)
    # print(pos, ''.join(message))
    # time.sleep(0.01)

  return ''.join(message), steps

def test():
  input = '''       │         
       |  +--+   
       A  |  C   
   F---|----E|--+
       |  |  |  D
       +B-+  +--+
'''
  start, data, letters = parse_input(input)
  # print(start, letters)
  # import pprint
  # pprint.pprint(data)
  result = traverse(start, data, letters)
  assert result[0] == "ABCDEF"
  assert result[1] == 38


test()
input = open('input.txt', 'r').read()
start, data, letters = parse_input(input)
# print(start, letters)
# import pprint
# pprint.pprint(input)
result = traverse(start, data, letters)
print(result[0])
print(result[1])
