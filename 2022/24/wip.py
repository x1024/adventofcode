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

MOD = 10000
def key(state):
  return ((state[0] * MOD + state[1].real) * MOD) + state[1].imag


def bfs(size, blizzards, start_tick, start, end):
  def enqueue(state):
    q.put((key(state), state))

  n, m = size
  q = queue.PriorityQueue()
  # Wait at the start, potentially a long time
  for tick in range(start_tick, start_tick + n*m + 1):
    enqueue((tick, start))

  seen = set()
  while not q.empty():
    _, state = q.get()
    if state in seen: continue
    seen.add(state)
    # print(state)
    tick, pos = state
    bstate = board_state(blizzards, tick + 1)
    for dir in movements:
      new_pos = pos + dir
      if new_pos == end: return tick + 1
      if new_pos.real < 0 or new_pos.imag < 0: continue
      if new_pos.real >= n or new_pos.imag >= m: continue
      if bstate[new_pos] != EMPTY: continue
      enqueue((tick + 1, new_pos))
  raise Exception("Path not found")


# data = data_test_2
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

start = complex(-1, 0)
end = complex(n, m-1)
tick1 = bfs(size, blizzards, 0, start, end)
tick2 = bfs(size, blizzards, tick1, end, start)
tick3 = bfs(size, blizzards, tick2, start, end)
result = tick3

print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
