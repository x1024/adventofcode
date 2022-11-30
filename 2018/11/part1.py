import pprint
import collections
import numpy


def solve(seed):
  # pprint.pprint(seed)

  data = {}
  for x in range(1, 300 + 1):
    for y in range(1, 300 + 1):
      pos = (x, y)
      data[pos] = fuel(x, y, seed)

  best = -1000;
  coords = (1, 1)
  for x in range(1, 300 + 1 - 2):
    for y in range(1, 300 + 1 - 2):
      pos = (x, y)
      total = (
        data[(x + 0, y + 0)] + 
        data[(x + 1, y + 0)] + 
        data[(x + 2, y + 0)] + 
        data[(x + 0, y + 1)] + 
        data[(x + 1, y + 1)] + 
        data[(x + 2, y + 1)] + 
        data[(x + 0, y + 2)] + 
        data[(x + 1, y + 2)] + 
        data[(x + 2, y + 2)])
      if total >= best:
        best = total
        coords = (x, y)
      best = max(best, total)

  return ','.join(map(str, coords))


def fuel(x, y, seed):
  '''
  • Find the fuel cell's rack ID, which is its X coordinate plus 10.
  • Begin with a power level of the rack ID times the Y coordinate.
  • Increase the power level by the value of the grid serial number (your puzzle
    input).
  • Set the power level to itself multiplied by the rack ID.
  • Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers
    with no hundreds digit become 0).
  • Subtract 5 from the power level.
  '''
  rack = (x + 10)
  power = rack * y
  power += seed
  power = power * rack
  power = int(((power % 1000) - (power % 100)) / 100 - 5)
  return power


def parse_line(input):
  return input.split()


def parse_input(input):
  return int(input)


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
