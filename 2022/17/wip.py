import IPython
import collections
import numpy
import pprint
import re


class Rock(object):
  rocks = [
    [ (0 + 0j), (1 + 0j), (2 + 0j), (3 + 0j), ],
    [ (0 + 1j), (1 + 1j), (2 + 1j), (1 + 0j), (1 + 2j), ],
    [ (0 + 0j), (1 + 0j), (2 + 0j), (2 + 1j), (2 + 2j), ],
    [ (0 + 0j), (0 + 1j), (0 + 2j), (0 + 3j), ],
    [ (0 + 0j), (1 + 0j), (0 + 1j), (1 + 1j), ],
  ]

  def __init__(self, pos, pattern):
    self.cells = [c + pos for c in Rock.rocks[pattern]]
  
  def move(self, offset, cave):
    # print(self.pos, self.cells)
    new_cells = [cell + offset for cell in self.cells]
    for c in new_cells:
      if cave[c] == WALL or c.real < 0 or c.real >= 7:
        return False
    self.cells = new_cells
    return True


def print_cave(cave, rock):
  max_y = int(max(i.imag for i,v in cave.items() if v == WALL))
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

WALL = '#'
EMPTY = '.'

def solve(data, turns):
  i = 0
  cave = collections.defaultdict((lambda: EMPTY), ((complex(x, 0), WALL) for x in range(7)))
  seen = {}
  LIMIT = 60 # empirically-discovered, your number might be different

  skipped_height = 0
  found_loop = False
  turn = -1
  while turn < turns:
    turn += 1
    rock_index = turn % len(Rock.rocks)
    wind_index = i % len(data)

    max_y = int(max(i.imag for i, v in cave.items() if v == WALL))
    cave = collections.defaultdict((lambda: EMPTY), ((k, v) for k, v in cave.items() if k.imag >= max_y - LIMIT))

    if not found_loop:
      key = (rock_index, wind_index, ''.join(cave.values()))
      if key in seen:
        found_loop = True
        previous_turn, previous_height = seen[key]
        modulo = turn - previous_turn
        height_diff = max_y - previous_height
        to_skip = (turns - turn) // modulo
        turn += to_skip * modulo
        skipped_height += to_skip * height_diff - 1
      else:
        seen[key] = (turn, max_y)

    rock = Rock(2 + (max_y + 4)*1j, rock_index)

    while True:
      wind_index = i % len(data)
      i += 1
      wind = data[wind_index]
      offset = 1 + 0j if wind == '>' else -1 + 0j
      rock.move(offset, cave)
      if not rock.move(0 - 1j, cave):
        for cell in rock.cells:
          cave[cell] = WALL
        break
  
  max_y = int(max(i.imag for i, v in cave.items() if v == WALL))
  return max_y + skipped_height


def test():
  input = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''
  result = solve(input, 2022)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
print(solve(input, 2022))
print(solve(input, 1000000000000))
