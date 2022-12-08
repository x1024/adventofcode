import pprint
import collections
import numpy


def solve(input):
  m = len(input)
  n = len(input[0])

  def score(x, y):
    t = input[x][y]
    good = True

    total = 1
    j = x - 1
    seen = 0
    while j >= 0:
      if input[j][y] >= t:
        seen += 1
        break
      if input[j][y] < t: seen += 1
      j -= 1
    total *= seen

    seen = 0
    j = x + 1
    while j < m:
      if input[j][y] >= t:
        seen += 1
        break
      if input[j][y] < t: seen += 1
      j += 1
    total *= seen

    seen = 0
    j = y - 1
    while j >= 0:
      if input[x][j] >= t:
        seen += 1
        break
      if input[x][j] < t: seen += 1
      j -= 1
    total *= seen

    seen = 0
    j = y + 1
    while j < n:
      if input[x][j] >= t:
        seen += 1
        break
      if input[x][j] < t: seen += 1
      j += 1
    total *= seen

    return total


  result = 0
  x = 1
  y = 0
  for x in range(m):
    for y in range(n):
      # print(x, y, input[x][y], isVisible(x, y))
      result = max(result, score(x, y))
  
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

