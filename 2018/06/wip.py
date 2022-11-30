import pprint
import collections
import numpy


def solve(input, DIST_LIMIT=10000):
  def check(x, y):
      total = 0
      for p in input:
        dx = abs(x - p[0])
        dy = abs(y - p[1])
        dist = dx + dy
        total += dist
        if total >= DIST_LIMIT:
          return 0
      return 1

  LIMIT = 1000
  total = 0
  for x in range(0, LIMIT * 2):
    print(x, total)
    for y in range(-LIMIT, LIMIT):
      total += check(x, y)
  return total


def parse_line(input):
  return tuple(int(i) for i in input.split(','))


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
1, 1    
1, 6    
8, 3    
3, 4    
5, 5    
8, 9    
  '''
  input = parse_input(input)
  result = solve(input, 32)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
