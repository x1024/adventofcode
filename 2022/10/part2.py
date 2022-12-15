import pprint
import collections
import numpy


def solve(input):
  # pprint.pprint(input)
  x = 1
  time = 0
  res = 0
  data = {}
  while time <= 240:
    c = input[time % len(input)]

    print(time, x, (time %40) in [x-1, x, x+1])
    if (time % 40) in [x - 1, x, x + 1]:
      data[time] = '#'
    else:
      data[time] = ' '
    time += 1
    if time % 40 == 20:
      res += (time * x)
      # print(res, time * x, time, x)

    if c[0] == 'noop':
      pass
    if c[0] == 'addx':
      x += c[1]

  print(data)
  screen = [
    ''.join([data[x] for x in range(0, 40)]),
    ''.join([data[x] for x in range(41, 80)]),
    ''.join([data[x] for x in range(81, 120)]),
    ''.join([data[x] for x in range(121, 160)]),
    ''.join([data[x] for x in range(161, 200)]),
    ''.join([data[x] for x in range(201, 240)]),
  ]
  print('\n'.join(screen))
  return res


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  res = []
  for row in input:
    row = row.split()
    if row[0] == 'noop':
      res.append(row)
    if row[0] == 'addx':
      res.append(('noop',))
      res.append((row[0], int(row[1])))
  # input = list(map(int, input))
  # input = list(map(parse_line, input))
  return res
  return input


def test():
  input = '''
  addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
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

import pyperclip
pyperclip.copy(str(result))

