import pprint
import collections
import numpy


def solve(steps):
  data = [3, 7]
  sa = 0
  sb = 1
  i = 0
  print(steps)
  while i < steps + 10:
    new = data[sa] + data[sb]
    # print(steps, sa, sb, data[sa], data[sb], data)
    if new >= 10:
      data.append(new // 10)
    data.append(new % 10)
    sa = (sa + 1 + data[sa]) % len(data)
    sb = (sb + 1 + data[sb]) % len(data)
    i += 1
  print(''.join(map(str, data[steps:steps+10])))
  return (''.join(map(str, data[steps:steps+10])))


def parse_line(input):
  return input.split()


def parse_input(input):
  return int(input)


def test():
  input = '''9'''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
