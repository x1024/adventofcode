import pprint
import collections
import numpy


def solve(input):
  pprint.pprint(input)
  m = len(input)
  n = len(input[0])
  def isVisible(x, y):
    t = input[x][y]
    good = True
    for j in range(0, x):
      if input[j][y] >= t: good = False
    if good: return True
    good = True
    for j in range(x + 1, m):
      if input[j][y] >= t: good = False
    if good: return True
    good = True
    for j in range(0, y):
      if input[x][j] >= t: good = False
    if good: return True
    good = True
    for j in range(y + 1, m):
      if input[x][j] >= t: good = False
    if good: return True
    return False

  result = 0
  x = 1
  y = 0
  for x in range(m):
    for y in range(n):
      # print(x, y, input[x][y], isVisible(x, y))
      result += isVisible(x, y)
  
  return result


def parse_line(input):
  return input


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [list(map(int, row)) for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
  30373
25512
65332
33549
35390
'''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

