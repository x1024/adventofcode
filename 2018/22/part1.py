import functools
import pprint
import collections
import numpy


@functools.cache
def geo_index(pos):
  if pos == start: return 0
  if pos == target: return 0
  if pos[0] == 0: return pos[1] * 48271
  if pos[1] == 0: return pos[0] * 16807
  print(pos, erosion_index((pos[0] - 1, pos[1])), erosion_index((pos[0], pos[1] - 1)))
  return erosion_index((pos[0] - 1, pos[1])) * erosion_index((pos[0], pos[1] - 1))

@functools.cache
def erosion_index(pos):
  return (geo_index(pos) + depth) % 20183

def tile(index):
  match index % 3:
    case 0: return '.'
    case 1: return '='
    case 2: return '|'



# test()
start = (0, 0)
lines = open('input.txt', 'r').read().strip().split("\n")
depth = int(lines[0].replace("depth: ", ""))
target = tuple(map(int, lines[1].replace("target: ", "").split(',')))

# depth = 510
# target = (10, 10)

# data = []
# for y in range(target[0] + 1):
#   row = ''.join(tile(erosion_index((x, y))) for x in range(target[1] + 1))
#   data.append(row)
# print('\n'.join(data))

print(start, target, depth)

print(sum(
  erosion_index((x, y)) % 3
    for x in range(target[0] + 1)
    for y in range(target[1] + 1)
))

print(start, target, depth)