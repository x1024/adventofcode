import functools
import pprint
import collections
import numpy
import IPython

def cmp(a, b):
  ia = type(a) == int
  ib = type(b) == int
  # print(a, b, ia, ib)
  if ia and ib:
    # print('both ints', a, b)
    if a < b: return 1
    if a > b: return -1
    return 0

  if ia:
    a = [a]
  if ib:
    b = [b]

  i = 0
  # print('comparing arrays', a, b)
  while i < len(a) and i < len(b):
    # print("cmp", a[i], b[i])
    res = cmp(a[i], b[i])
    if res: return res
    i += 1
  if len(a) < len(b): return 1
  if len(a) > len(b): return -1
  return 0

def solve(input):
  result = 0
  input.sort(key=functools.cmp_to_key(cmp))
  input = list(reversed(input))
  a = input.index([[2]]) + 1
  b = input.index([[6]]) + 1
  return a * b


def parse_line(input):
  return input.split()


def parse_input(input):
  dividers = '''[[2]]
[[6]]
'''
  input = dividers + input
  lists = []
  for row in input.split('\n'):
    if not row: continue
    lists.append(eval(row))
  return lists


def test():
  input = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''
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

IPython.embed()
