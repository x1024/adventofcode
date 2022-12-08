import pprint
import collections
import numpy


def solve(input):
  pprint.pprint(input)
  for i, c in enumerate(input):
    s = set(input[i:i+14])
    if len(s) == 14:
      print(i+14)
      return i+14
  return 0


def parse_line(input):
  return input.split()


def parse_input(input):
  # input = input.split('\n')
  # input = [row.strip() for row in input]
  # input = [row for row in input if row]
  # # input = list(map(int, input))
  # input = list(map(parse_line, input))
  return input


def test():
  input = '''nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'''
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

