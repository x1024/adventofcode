import pprint
import collections
import re
import numpy

def distance(pos_a, pos_b):
  return (
    abs(pos_a[0] - pos_b[0]) + 
    abs(pos_a[1] - pos_b[1]) + 
    abs(pos_a[2] - pos_b[2])
  )

def solve(bots):
  max_r = 0
  best_bot = bots[0]
  for bot in bots:
    if bot[1] > max_r:
      max_r = bot[1]
      best_bot = bot

  result = sum(distance(best_bot[0], bot[0]) <= best_bot[1] for bot in bots)
  return result


def parse_line(input):
  pos, radius = input.replace("pos=<", "").split(">, r=")
  pos = list(map(int, pos.split(',')))
  radius =int(radius)
  return pos, radius


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
'''.strip("\n")
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  exit()


# test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
