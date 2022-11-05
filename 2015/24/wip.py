import itertools
import operator
import functools

def product(lst):
  res = 1
  for a in lst:
    res *= a
  return res


def solve(input, group_size):
  total = sum(input) // group_size
  for size in range(1, len(input) + 1):
    for c in itertools.combinations(input, size):
      if sum(c) == total:
        return functools.reduce(operator.mul, c, 1)


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  input = list(map(int, input))
  # input = map(parse_line, input)
  return input


def test():
  input = '''
  1
  2
  3
  4
  5
  7
  8
  9
  10
  11
  '''
  input = parse_input(input)
  print(solve(input, 3))
  print(solve(input, 4))
  return


test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
print(solve(input, 3))
print(solve(input, 4))