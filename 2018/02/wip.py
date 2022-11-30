import pprint
import collections
import itertools
import numpy

def solve(input):
  for wa, wb in itertools.product(input, input):
    common = ''.join(a for a, b in zip(wa, wb) if a == b)
    if len(common) + 1 == len(wa):
      return common
  return 0


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  return input


input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
