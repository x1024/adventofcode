import pprint
import collections
import numpy


def solve(input):
  LIMIT = 1000
  data = []
  for x in range(LIMIT):
    data.append([0] * LIMIT)

  for id, start, size in input:
    for x in range(start[0], start[0] + size[0]):
      for y in range(start[1], start[1] + size[1]):
        # print(x, y)
        data[x][y] += 1
  # pprint.pprint(data)
  count = 0
  for row in data:
    for cell in row:
      if cell > 1:
        count += 1
  return count


def parse_line(input):
  id, dimensions = input.split(' @ ')
  start, size = dimensions.split(': ')
  start = [int(i) for i in start.split(',')]
  size = [int(i) for i in size.split('x')]
  # print(id, start, size)
  return (id, start, size)


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
