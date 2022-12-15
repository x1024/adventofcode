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
  for i, group in enumerate(input):
    print("-----")
    print(i+1, cmp(*group), group)
    if cmp(*group) == 1:
      result += i + 1

  return result


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split('\n\n')
  data = []
  for group in input:
    lists = []
    for row in group.split('\n'):
      l = eval(row)
      # print(row)
      # print(l)
      lists.append(l)
    data.append(lists)
  return data


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
