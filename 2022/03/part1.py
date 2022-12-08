import pprint
import collections
import numpy


def solve(input):
  res = 0
  for row in input:
    print(row)
    row = row[0]
    print(row)
    l = len(row) // 2
    print(l)
    a, b = (row[l:], row[:l])
    print(a, b)
    for x in range(26):
      c = chr(ord('a') + x)
      if c in a and c in b:
        res += x + 1
        print(c)
    for x in range(26):
      c = chr(ord('A') + x)
      if c in a and c in b:
        res += x + 1 + 26
        print(c)
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

