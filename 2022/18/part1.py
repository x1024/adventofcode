import IPython
import collections
import numpy
import pprint
import re

offsets = [
  (1, 0, 0),
  (-1, 0, 0),
  (0, 1, 0),
  (0, -1, 0),
  (0, 0, 1),
  (0, 0, -1),
]

def solve(input):
  pprint.pprint(input)
  result = 0
  for cube in input:
    for offset in offsets:
      new_cube = cube[0] + offset[0], cube[1] + offset[1], cube[2] + offset[2]
      if new_cube not in input:
        result += 1
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
  2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
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
