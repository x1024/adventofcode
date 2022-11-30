import pprint
import collections
import numpy


def solve(seed):
  LIMIT = 300

  data = []
  data.append([0] * (LIMIT + 1))
  for _ in range(LIMIT + 1):
    data.append([0] * (LIMIT + 1))

  for x in range(1, LIMIT + 1):
    for y in range(1, LIMIT + 1):
      data[x][y] = fuel(x, y, seed)

  for x in range(1, LIMIT):
    for y in range(1, LIMIT):
      data[x][y] = data[x][y] + data[x-1][y] + data[x][y-1] - data[x-1][y-1]

  best = -10 * LIMIT * LIMIT * 10;
  coords = (1, 1, 1)
  size = 3

  for size in range(1, LIMIT + 1):
    for x in range(size - 1, LIMIT):
      for y in range(size - 1, LIMIT):
        total = data[x][y] - data[x-size][y] - data[x][y-size] + data[x-size][y-size]
        if total >= best:
          # print (coords, total, best)
          best = total
          coords = (x - size + 1, y - size + 1, size)

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
