import pprint
import collections
import numpy
import IPython


def solve(monkeys, rounds=10000):
  r = 1
  for m in monkeys:
    r *= m.test
  Monkey.modulo = r
  for i in range(rounds):
    for m in monkeys:
      m.do_round()
  data = list(sorted([m.inspected for m in monkeys]))[::-1]
  return data[0] * data[1]


def parse_line(input):
  return input.split()


def parse_input(input):
  monkeys = input.split('\n\n')
  all = []
  for m in monkeys:
    m = m.split("\n")
    index = int(m[0].split(" ")[-1].strip(":"))
    items = list(map(int, m[1].split(":")[-1].split(", ")))
    test = int(m[3].split(" ")[-1])
    operation = m[2].split(": ")[-1]
    t = int(m[4].split(" ")[-1])
    f = int(m[5].split(" ")[-1])
    M = Monkey(index, items, operation, test, t, f)
    all.append(M)
  return all


class Monkey(object):
  all = {}
  def __init__(self, index, items, operation, test, t, f):
    Monkey.all[index] = self
    self.index = index
    self.items = items
    self.operation = operation.split(" = ")[-1]
    self.test = test
    self.true = t
    self.false = f
    self.inspected = 0
  
  def do_round(self):
    for item in self.items:
      self.inspected += 1
      old = item # needed for eval()
      r = eval(self.operation)
      # r //= 3
      r = r % Monkey.modulo
      Monkey.all[self.true if r % self.test == 0 else self.false].items.append(r)
    self.items = []


input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)

print("")
print("-------------")
print("Result: {}".format(result))
print("-------------")
print("")

import pyperclip
pyperclip.copy(str(result))
IPython.embed()
