import pprint
import collections
import numpy


def solve(input):
  return sum(sorted(input)[-3:])


def parse_line(input):
  return sum(map(int, input.split('\n')))


def parse_input(input):
  return list(map(parse_line, input.split('\n\n')))


def test():
  input = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'''
  input = parse_input(input)
  result = solve(input)
  print(result)
  assert result == 45000
  return


test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
