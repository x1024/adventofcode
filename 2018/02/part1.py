import pprint
import collections

def solve(input):
  # pprint.pprint(input)
  twos = [i for i in input if 2 in i.values()]
  threes = [i for i in input if 3 in i.values()]
  print(len(twos))
  print(len(threes))
  return len(twos) * len(threes)
  return 0


def parse_line(input):
  return collections.Counter(input)
  return input.split()


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
