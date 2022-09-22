import json

def parse_input(input):
  # input = input.split('\n')
  # input = [row.strip() for row in input]
  # input = [row for row in input if row]
  # input = map(int, input)
  return json.loads(input)
  return input

def solve(input):
  print type(input)
  if type(input) == int:
    return input
  if type(input) == list:
    return sum(solve(key) for key in input)
  if type(input) == dict:
    return sum(solve(key) for key in input.values())
  # print input
  # print input
  return 0

input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
