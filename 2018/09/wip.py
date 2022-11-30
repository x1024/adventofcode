import pprint
import collections
import numpy

class L(object):
  def __init__(self, value):
    self.value = value
    self.prev = self
    self.next = self
  
  def insert(self, other):
    n = self.next
    self.next = other
    other.next = n
    n.prev = other
    other.prev = self
    return other

  def remove(self):
    p = self.prev
    n = self.next
    p.next = n
    n.prev = p
    return n


def solve(players, marbles):
  # pprint.pprint(input)
  i = 0

  list = L(0)

  scores = [0] * players
  while i <= marbles:
    i += 1
    # print_list(list)
    if i % 23 == 0:
      player = (i - 1) % players
      scores[player] += i
      # print(list.value)
      for _ in range(7):
        list = list.prev
        # print(list.value)
      # print(i, list.value)
      scores[player] += list.value
      list = list.remove()
      if i % 23000 == 0:
        print("%d%%" % int(100 * i / marbles))
    else:
      list = list.next
      now = L(i)
      list = list.insert(now)

  return max(scores)


def print_list(l):
  start = l.value
  while True:
    l = l.next
    print(l.value, end=' ')
    if start == l.value:
      break
  print()

def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split()
  players = int(input[0])
  marbles = int(input[-2])
  return players, marbles


def test():
  input = '''10 players; last marble is worth 1618 points'''
  # input = '''9 players; last marble is worth 25 points'''
  input = parse_input(input)
  result = solve(*input)
  print("Test Result: {}".format(result))
  return


test()
input = open('input.txt', 'r').read().strip()
players, marbles = parse_input(input)
result = solve(players, marbles * 100)
print("Result: {}".format(result))
