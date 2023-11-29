import queue
import IPython
import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()
data_test = '''
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
'''
data_test_2 = '''
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
'''
WALL = '#'
EMPTY = '.'
DOWN = 'v'
UP = '^'
LEFT = '<'
RIGHT = '>'
PLAYER = '@'


directions = {
  UP:    (-1 + 0j),
  DOWN:  (+1 + 0j),
  LEFT:  ( 0 - 1j),
  RIGHT: ( 0 + 1j),
}

movements = [
  ( 0 + 0j),
  (-1 + 0j),
  (+1 + 0j),
  ( 0 - 1j),
  ( 0 + 1j),
]

dir_map = {
  (-1 + 0j): UP,
  (+1 + 0j): DOWN,
  ( 0 - 1j): LEFT,
  ( 0 + 1j): RIGHT,
}


def print_board(size, blizzards, tick, player_pos=None):
  board = board_state(blizzards, tick)

  print()
  print("*" * (size[1] + 2))
  for x in range(size[0]):
    print("*", end="")
    for y in range(size[1]):
      pos = complex(x, y)
      print(PLAYER if pos == player_pos else board[pos], end="")
    print("*")
  print("*" * (size[1] + 2))


memo = {}
def board_state(blizzards, tick):
  if tick in memo: return memo[tick]

  board = collections.defaultdict(lambda: EMPTY)
  for pos, direction in blizzards:
    pos = (pos + direction * tick)
    pos = complex(int(pos.real % size[0]), int(pos.imag % size[1]))
    board[pos] = dir_map[direction]

  memo[tick] = board
  return board


def bfs(size, blizzards):
  n, m = size
  start = complex(-1, 0)
  end = complex(n, m-1)
  # print(start)
  # print(end)
  q = queue.Queue()
  tick = 0
  while True:
    state = board_state(blizzards, tick + 1)
    # print(tick)
    # print_board(size, blizzards, tick + 1)
    if state[start + directions[DOWN]] == EMPTY:
      q.put((tick, start))
      print("Start at: ", tick, start)
      break
    tick += 1

  i = 0
  while not q.empty():
    tick, pos = q.get()
    state = board_state(blizzards, tick + 1)
    i += 1
    if i % 10000 == 0:
      print(i, tick, pos, size)
    # print_board(size, blizzards, tick, pos)
    # print_board(size, blizzards, tick + 1)
    for dir in movements:
      new_pos = pos + dir
      if new_pos == end:
        print("Found it!", tick + 1)
        return tick + 1
      if new_pos.real < 0 or new_pos.imag < 0: continue
      if new_pos.real >= n or new_pos.imag >= m: continue
      if state[new_pos] != EMPTY: continue
      q.put((tick + 1, new_pos))


# data = data_test_2
# data[0][1] = WALL
data = data.strip("\n").split('\n')
n = len(data) - 2
m = len(data[0]) - 2
size = (n, m)
blizzards = []
for i, row in enumerate(data):
  for j, col in enumerate(row):
    if col == WALL or col == EMPTY: continue
    pos = complex(i - 1, j - 1)
    direction = directions[col]
    blizzards.append((pos, direction))

# print_board(size, blizzards, 0, (0 + 0j))
# exit()

import os
import time

tick = 0
while True:
    print_board(size, blizzards, tick)
    tick += 1
    time.sleep(0.2)
    os.system('cls')

# pprint.pprint(data)
result = bfs(size, blizzards)
print(result)



print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
