import pprint
import collections
import numpy

def solve(input):
  _, tree = parse(input)
  pprint.pprint(tree)
  print(checksum(tree))
  return checksum(tree)


def checksum(tree):
  children, metadata = tree
  return sum(metadata) + sum(checksum(child) for child in children)


def parse(input):
  num_children = input[0]
  num_metadata = input[1]
  input = input[2:]
  children = []
  for _ in range(num_children):
    input, child = parse(input)
    children.append(child)

  metadata = input[:num_metadata]
  input = input[num_metadata:]

  res = (children, metadata)
  return input, res


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split(' ')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  input = list(map(int, input))
  # input = list(map(parse_line, input))
  return input


def test():
  input = '''
  2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
