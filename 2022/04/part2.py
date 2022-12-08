import pprint
import collections
import numpy


def solve(input):
  result = 0
  for row in input:
    print(row)
    a, b = row
    c = max(a[0], b[0])
    d = min(a[1], b[1])
    print(c, d)
    if c <= d: result += 1
  
  return result


def parse_line(input):
  return [list(map(int,c.split('-'))) for c in input.split(',')]


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

