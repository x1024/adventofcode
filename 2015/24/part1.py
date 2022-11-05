import itertools

def solve(input):
  total = sum(input) // 3
  options = []
  for size in range(1, len(input) + 1):
    if options:
      break
    for c in itertools.combinations(input, size):
      if sum(c) == total:
        options.append(c)

  solutions = []
  for option in options:
    rest = [x for x in input if x not in option]
    print(option, rest)
    found = False
    for size in range(1, len(rest) + 1):
      if found: break
      for c in itertools.combinations(rest, size):
        if sum(c) == total:
          solutions.append(option)
          found = True
          break
  print(solutions)
  def product(lst):
    res = 1
    for a in lst:
      res *= a
    return res
  print(min(product(s) for s in solutions))
  return 0


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
  result = solve(input)
  print("Test Result: {}".format(result))
  return


test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
