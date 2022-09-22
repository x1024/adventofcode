
import functools
#functools.cache

def solve(containers, limit=150):
  l = len(containers)
  total = 0
  for i in range(2**l):
    tmp = 0
    for j in range(l):
      if i & (2**j):
        tmp += containers[j]
    total += tmp == limit
    if i % 1000 == 0:
      print(i, 2**l, tmp, total)
  return total


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  input = map(int, input)
  input = list(input)
  # input = map(parse_line, input)
  return input


def test():
  input = '''
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
# print(solve(( 20, 15, 10, 5, 5 ), 25))
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
