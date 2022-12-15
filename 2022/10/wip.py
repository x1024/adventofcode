import collections


def easy(input):
  x = 1
  checksum = 0
  for time, value in enumerate(input):
    if (time + 1) % 40 == 20: checksum += (time + 1) * x
    x += value
  return checksum


def hard(input, ROW_SIZE=40):
  x = 1
  data = collections.defaultdict(lambda: ' ')
  for time, value in enumerate(input):
    if x - 1 <= (time % 40) <= x + 1: data[time] = '█'
    x += value
  return ('\n'.join(''.join([data[cell]
    for cell in range(row * ROW_SIZE, (row + 1) * ROW_SIZE)])
    for row in range(len(input) // ROW_SIZE)
  ))


def parse_input(input):
  for row in input.split("\n"):
    yield 0
    if row.startswith('addx'):
      yield int(row.split()[1])


input = open('input.txt', 'r').read().strip()
input = list(parse_input(input))
print(easy(input))
print(hard(input))