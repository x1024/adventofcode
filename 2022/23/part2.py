import IPython
import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()
data_test = '''
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
'''

# data_test = '''
# .....
# ..##.
# ..#..
# .....
# ..##.
# .....'''

N =  (-1 + 0j)
S =  (+1 + 0j)
W =  (+0 - 1j)
E =  (+0 + 1j)
NW = N + W
NE = N + E
SW = S + W
SE = S + E

all_dirs = [N, S, W, E, NW, NE, SW, SE,]
dirs = [
  [N, NE, NW],
  [S, SE, SW],
  [W, NW, SW],
  [E, NE, SE],
]

EMPTY = '.'
ELF = '#'

def checksum(board):
  minx = int(min(b.real for b, v in board.items() if v == ELF))
  maxx = int(max(b.real for b, v in board.items() if v == ELF))
  miny = int(min(b.imag for b, v in board.items() if v == ELF))
  maxy = int(max(b.imag for b, v in board.items() if v == ELF))
  res = 0
  for x in range(minx, maxx + 1):
    for y in range(miny, maxy + 1):
      res += board[complex(x, y)] == EMPTY
  return res

def print_board(board):
  minx = int(min(b.real for b, v in board.items() if v == ELF))
  maxx = int(max(b.real for b, v in board.items() if v == ELF))
  miny = int(min(b.imag for b, v in board.items() if v == ELF))
  maxy = int(max(b.imag for b, v in board.items() if v == ELF))
  for x in range(minx, maxx + 1):
    for y in range(miny, maxy + 1):
      print(board[complex(x, y)], end="")
    print()
  print()

# data = data_test
data = data.strip("\n").split('\n')
data = [row.strip() for row in data]
# data = list(map(int, data))
board = collections.defaultdict(lambda: EMPTY)
for i, row in enumerate(data):
  for j, cell in enumerate(row):
    board[complex(i, j)] = cell

def iterate(turn, board):
  l = len(dirs)
  elves = [pos for pos, value in board.items() if value == ELF]
  goal = {}
  seen = collections.defaultdict(lambda: 0)
  moved = 0
  for pos in elves:
    if all(board[pos + offset] == EMPTY for offset in all_dirs):
      goal[pos] = False
      continue

    for i in range(l):
      dir = dirs[(turn + i) % l]
      if all(board[pos + offset] == EMPTY for offset in dir):
        new_pos = pos + dir[0]
        goal[pos] = new_pos
        seen[new_pos] += 1
        # print("Elf goal:", pos, new_pos)
        break

  for pos, target in goal.items():
    # print(pos, target, seen[target])
    if target is not False and seen[target] < 2:
      # print("PLACING ELF", pos, target)
      board[pos] = EMPTY
      board[target] = ELF
      moved += 1
    else:
      pass
      # print("ELF NO MOVE", pos)

  return moved

# pprint.pprint(data)
print_board(board)
turn = 0
while True:
  moved = iterate(turn, board)
  if moved == 0: break
  turn += 1
  # print_board(board)
  print(turn, moved, checksum(board))
result = turn + 1
print(result)


print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
