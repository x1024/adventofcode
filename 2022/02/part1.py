import pprint
import collections
import numpy


def solve(input):
  score = 0
  data = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C',
  }
  win = {
    'A': 'C',
    'B': 'A',
    'C': 'B',
  }
  for a, b in input:
    b = data[b]
    print(score)
    round = ord(b) - ord('A') + 1
    if a == b:
      round += 3
    elif win[b] == a:
      round += 6
    print(a, b, win[b], round)
    score += round

  return score


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
  A Y
B X
C Z
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
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

