import queue
import IPython
import collections
import numpy
import pprint
import re
import sys

sys.setrecursionlimit(10000)

offsets = [
  (1, 0, 0),
  (-1, 0, 0),
  (0, 1, 0),
  (0, -1, 0),
  (0, 0, 1),
  (0, 0, -1),
]

i = 0
def solve(input):
  # pprint.pprint(input)
  result = 0
  pos_min = [
    (min(c[0] for c in input)),
    (min(c[1] for c in input)),
    (min(c[2] for c in input)),
  ]
  pos_max = [
    (max(c[0] for c in input)),
    (max(c[1] for c in input)),
    (max(c[2] for c in input)),
  ]

  MIN = min(pos_min)
  MAX = max(pos_max)
  print(MIN, MAX)
  q = queue.Queue()
  air_pocket = set()
  empty = set()

  def bfs(start):
    if start in input: return
    if start in empty: return
    global i
    seen = set()

    q.put(start)
    is_outside = False
    while not q.empty():
      cube = q.get()
      i += 1
      if cube in input: continue
      if cube in seen: continue
      seen.add(cube)
      if cube[0] <= MIN or cube[1] <= MIN or cube[2] <= MIN:
        is_outside = True
        continue
      elif cube[0] >= MAX or cube[1] >= MAX or cube[2] >= MAX:
        is_outside = True
        continue

      for offset in offsets:
        new_cube = cube[0] + offset[0], cube[1] + offset[1], cube[2] + offset[2]
        q.put(new_cube)

    if is_outside:
      for c in seen: empty.add(c)
    else:
      print("INSIDE")
      print(seen)
      for c in seen: air_pocket.add(c)
      return seen

  for x in range(MIN, MAX + 1):
    for y in range(MIN, MAX + 1):
      for z in range(MIN, MAX + 1):
        cube = (x, y, z)
        print(x, y, z)
        bfs(cube)

  for cube in input:
    r = 0
    for offset in offsets:
      new_cube = cube[0] + offset[0], cube[1] + offset[1], cube[2] + offset[2]
      if new_cube in input:
        continue
      elif new_cube in air_pocket:
        continue
      r += 1
    print(cube, r)
    result += r

  return result


def parse_line(input):
  # return tuple(map(int, re.findall("[-\d]+", input)))
  return tuple(map(int, input.split(',')))


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  input = set(input)
  return input


def test():
  input = '''
1,2,2
1,2,5
2,1,2
2,1,5
2,2,1
2,2,2
2,2,3
2,2,4
2,2,6
2,3,2
2,3,5
3,2,2
3,2,5
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
