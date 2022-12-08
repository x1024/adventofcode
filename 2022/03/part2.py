import pprint
import collections
import numpy


def solve(input):
  res = 0
  for i in range(0, len(input), 3):
    rows = input[i:i+3]
    q, w, e = [row[0] for row in rows]
    print(q, w, e)
    for x in range(26):
      c = chr(ord('a') + x)
      if c in q and c in w and c in e:
        res += x + 1
        print(c)
    for x in range(26):
      c = chr(ord('A') + x)
      if c in q and c in w and c in e:
        res += x + 1 + 26
        print(c)
    # row = row[0]
    # print(row)
    # l = len(row) // 2
    # print(l)
    # a, b = (row[l:], row[:l])
    # print(a, b)
  return res


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
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

import pyperclip
pyperclip.copy(str(result))

