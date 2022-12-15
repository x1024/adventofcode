import collections


ROW_SIZE = 40


def solve(input):
  input = list(input)
  x = 1
  checksum = 0
  screen = [list(' ' * ROW_SIZE) for _ in range(len(input) // ROW_SIZE)]
  for time, value in enumerate(input):
    if abs(time % 40 - x) <= 1: screen[time // ROW_SIZE][time % 40] = '#'
    if (time + 1) % 40 == 20: checksum += ((time + 1) * x)
    x += value

  return checksum, ('\n'.join(''.join(row) for row in screen))


def parse_input(input):
  for row in input.split("\n"):
    yield 0
    if row.startswith('addx'):
      yield int(row.split()[1])


input = open('input.txt', 'r').read().strip()
input = parse_input(input)
checksum, code = solve(input)
print(checksum)
print(code)