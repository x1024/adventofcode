def solve(input):
  print input
  return 0


def parse_line(input):
  return input.split()


def parse_input(input):
  # input = input.split('\n')
  # input = [row.strip() for row in input]
  # input = [row for row in input if row]
  # input = map(int, input)
  # input = map(parse_line, input)
  return input


def test():
  input = '''
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
