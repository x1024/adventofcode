import pprint
import collections
import numpy


def solve(steps):
  data = [3, 7]
  sa = 0
  sb = 1
  i = 0
  l = len(str(steps))
  check = list(map(int, str(steps)))
  print(check, steps)
  while True:
    new = data[sa] + data[sb]
    if i % 1000000 == 0: print(i)
    # print(steps, sa, sb, data[sa], data[sb], data)
    if new >= 10:
      data.append(new // 10)
      if data[-l:] == check:
        print(i, data[-l:], check)
        return len(data) - l
    data.append(new % 10)
    if data[-l:] == check:
      print(i, data[-l:], check)
      return len(data) - l

    sa = (sa + 1 + data[sa]) % len(data)
    sb = (sb + 1 + data[sb]) % len(data)
    i += 1


def parse_line(input):
  return input.split()


def parse_input(input):
  return int(input)


def test():
  input = '59414'
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
