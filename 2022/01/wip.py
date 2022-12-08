def solve(input):
  input = sorted(input)
  return sum(input[-3:])

def parse_line(input):
  return sum(map(int, input.split('\n')))

def parse_input(input):
  input = input.split('\n\n')
  # input = [row.strip() for row in input]
  # input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input

import pyperclip
import pprint
import collections
import numpy

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

pyperclip.copy(str(result))
