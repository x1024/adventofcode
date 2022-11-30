import pprint
import collections
import numpy


def solve(input):
  lower = 'abcdefghijklmnopqrstuvwxyz'
  upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  to_replace = []
  for l in zip(lower, upper):
    to_replace.append(''.join(l))
    to_replace.append(''.join(l[::-1]))
  print(to_replace)
  while True:
    l = len(input)
    for r in to_replace:
      input = input.replace(r, '')
    if l == len(input):
      return len(input)


def parse_line(input):
  return input.split()


def parse_input(input):
  return input
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
