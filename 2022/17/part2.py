import IPython
import collections
import numpy
import pprint
import re

rocks = [
'''
####
''',

'''
.#.
###
.#.
''',

'''
..#
..#
###
''',

'''
#
#
#
#
''',

'''
##
##
'''
]

rock0 = [
  # ####
  (0 + 0j),
  (1 + 0j),
  (2 + 0j),
  (3 + 0j),
]

'''
.#.
###
.#.
''',
rock1 = [
  (0 + 1j),
  (1 + 1j),
  (2 + 1j),
  (1 + 0j),
  (1 + 2j),
]

'''
..#
..#
###
''',
rock2 = [
  (0 + 0j),
  (1 + 0j),
  (2 + 0j),
  (2 + 1j),
  (2 + 2j),
]

'''
#
#
#
#
''',
rock3 = [
  (0 + 0j),
  (0 + 1j),
  (0 + 2j),
  (0 + 3j),
]

'''
##
##
'''
rock4 = [
  (0 + 0j),
  (1 + 0j),
  (0 + 1j),
  (1 + 1j),
]

rocks = [
  rock0, rock1, rock2, rock3, rock4
]

class Rock(object):
  def __init__(self, pos, cells):
    self.pos = pos
    self.cells = [c + pos for c in cells]
  
  def move(self, offset, cave):
    # print(self.pos, self.cells)
    self.pos += offset
    new_cells = [cell + offset for cell in self.cells]
    for c in new_cells:
      if cave[c] == '#' or c.real < 0 or c.real >= 7:
        return False
    self.cells = new_cells
    return True


def print_cave(cave, rock):
  max_y = int(max(i.imag for i,v in cave.items() if v == '#'))
  for y in range(max_y + 8, 0 - 1, -1):
    print("#", end='')
    for x in range(7):
      c = complex(x, y)
      if c in rock.cells:
        print("@", end='')
      else:
        print(cave[c], end='')
    print("#")
  print("")
  print("")


def solve(data, turns):
  i = 0
  max_y = 0
  cave = collections.defaultdict(lambda: '.')
  # print(len(data), len(rocks))
  for x in range(7):
    cave[complex(x, 0)] = '#'
  import time
  seen = {}
  # turns = 20

  height_to_skip = 0
  found = False
  turn = 0
  while turn < turns:
    rock_index = turn % len(rocks)
    pattern = rocks[rock_index]
    max_y = int(max(i.imag for i, v in cave.items() if v == '#'))
    # if turn % 100 == 0: print(turn, max_y, height_to_skip, "%.2f" % (turn * 100 / turns))
    top_rows = '\n'.join(
      ''.join(cave[complex(i, y)] for i in range(7))
      for y in range(max_y - 30, max_y + 1)
    )

    wind_index = i % len(data)
    key = (top_rows, rock_index, wind_index)
    if key in seen and not found:
      found = True
      # print ("FOUND IIIT", turn, key)
      previous_turn, previous_height = seen[key]
      modulo = turn - previous_turn
      height_diff = max_y - previous_height
      # print(modulo, height_diff)
      to_skip = (turns - turn) // modulo
      turn += to_skip * modulo
      height_to_skip += to_skip * height_diff

    seen[key] = (turn, max_y)
    # print(max_y)
    rock = Rock(complex(2, max_y + 4), pattern)
    # print("New Rock")
    # print_cave(cave, rock)

    while True:
      wind_index = i % len(data)
      wind = data[wind_index]
      offset = 1 + 0j if wind == '>' else -1 + 0j
      # print(turn, wind, offset, rock.pos)
      # print(i, wind, "Rock moves horizontally", offset)
      rock.move(offset, cave)
      # print(rock.pos, rock.cells)
      # print_cave(cave, rock)
      # move down
      # print("Rock moves down")
      i += 1
      if not rock.move(0 - 1j, cave):
        # rock won't fall anymore
        for cell in rock.cells:
          cave[cell] = '#'
        # print_cave(cave, rock)
        break
      # print_cave(cave, rock)

    turn += 1
  
  max_y = int(max(i.imag for i, v in cave.items() if v == '#'))
  return max_y + height_to_skip


def parse_line(input):
  # return tuple(map(int, re.findall("[-\d]+", input)))
  return input.split()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''
  result = solve(input, 2022)
  print("Test Result: {}".format(result))
  result = solve(input, 1000000000000)
  print("Test Result: {}".format(result))
  assert result == 1514285714288
  return


test()
input = open('input.txt', 'r').read().strip()
print(solve(input, 2022))
result = solve(input, 1000000000000)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# IPython.embed()
