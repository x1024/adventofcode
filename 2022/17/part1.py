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

def parse_rock(rock):
  rows = [row for row in rock.split("\n") if row]
  print(rows)


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


def solve(data, turns=2022):
  i = 0
  max_y = 0
  cave = collections.defaultdict(lambda: '.')
  for x in range(7):
    cave[complex(x, 0)] = '#'

  for turn in range(turns):
    pattern = rocks[turn % len(rocks)]
    max_y = int(max(i.imag for i, v in cave.items() if v == '#')) + 4
    print(turn, max_y)
    # print(max_y)
    rock = Rock(complex(2, max_y), pattern)
    # print("New Rock")
    # print_cave(cave, rock)

    while True:
      wind = data[i % len(data)]
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
  
  max_y = int(max(i.imag for i, v in cave.items() if v == '#'))
  return max_y


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
  result = solve(input)
  print("Test Result: {}".format(result))
  return


test()
# exit()
input = open('input.txt', 'r').read().strip()
result = solve(input)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# IPython.embed()
