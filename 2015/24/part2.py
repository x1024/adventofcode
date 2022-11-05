import itertools

def product(lst):
  res = 1
  for a in lst:
    res *= a
  return res


def solve(input, group_size):
  suma = sum(input)
  if suma % group_size != 0: return False
  total = suma // group_size
  print(suma, group_size, total, input, suma % group_size)
  options = []
  for size in range(1, len(input) + 1):
    if options:
      break
    for c in itertools.combinations(input, size):
      if sum(c) == total:
        options.append(c)

  if group_size == 2:
    if not options:
      return False
    return min(product(o) for o in options)

  solutions = []
  for option in options:
    rest = [x for x in input if x not in option]
    solve_rest = solve(rest, group_size - 1)
    if solve_rest:
      solutions.append(option)
  if not solutions:
    return False
  return min(product(s) for s in solutions)


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
  result = solve(input, 4)
  print("Test Result: {}".format(result))
  return


test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input, 4)
print("Result: {}".format(result))
