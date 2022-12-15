import pprint
import collections
import numpy
import IPython


def solve(monkeys, rounds=10000):
  r = 1
  for m in monkeys:
    print(m.test)
    r *= m.test
  print(r)
  # 9699690
  Monkey.modulo = r
  for i in range(rounds):
    print(i)
    for m in monkeys:
      m.do_round()
  for m in monkeys:
    print (m.index, m.items)
  for m in monkeys:
    print (m.index, m.inspected)
  data = list(sorted([m.inspected for m in monkeys]))[::-1]
  return data[0] * data[1]

def parse_line(input):
  return input.split()


def parse_input(input):
  monkeys = input.split('\n\n')
  all = []
  for m in monkeys:
    # print(m)
    m = m.split("\n")
    # print(m)
    index = int(m[0].split(" ")[-1].strip(":"))
    items = list(map(int, m[1].split(":")[-1].split(", ")))
    test = int(m[3].split(" ")[-1])
    operation = m[2].split(": ")[-1]
    t = int(m[4].split(" ")[-1])
    f = int(m[5].split(" ")[-1])
    # print(index, items, operation, test, t, f)
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
      old = item
      r = eval(self.operation)
      # r //= 3
      # print(self.index, item, r, r % self.test, self.true, self.false)
      r = r % Monkey.modulo
      if r % self.test == 0:
        # print("YES", self.true, Monkey.all[self.true].index, r)
        Monkey.all[self.true].items.append(r)
      else:
        # print("NO", self.false, Monkey.all[self.true].index, r)
        Monkey.all[self.false].items.append(r)
    self.items = []


def test():
  input = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
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

print("")
print("-------------")
print("Result: {}".format(result))
print("-------------")
print("")

import pyperclip
pyperclip.copy(str(result))
IPython.embed()