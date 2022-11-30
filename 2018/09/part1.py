import pprint
import collections
import numpy


def solve(players, marbles):
  pprint.pprint(input)
  i = 0
  data = [0]
  current = 0
  scores = [0] * players
  while i <= marbles:
    i += 1
    if i % 23 == 0:
      player = (i - 1) % players
      scores[player] += i
      current = (current - 7 + len(data)) % len(data)
      scores[player] += data[current]
      print(i, data[current])
      data = data[:current - 1] + data[current:]
    else:
      current = (current + 2) % len(data)
      data.insert(current, i)

  print(scores)
  return max(scores)


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


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(*input)
print("Result: {}".format(result))
