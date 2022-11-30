import pprint
import collections

def solve(input):
  i = 0
  seen = set()
  suma = 0
  print(input)
  while True:
    suma += input[i % len(input)]
    i += 1
    if suma in seen: return suma
    seen.add(suma)
  return sum(input)


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
