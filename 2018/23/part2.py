import z3
from z3 import *
from collections import defaultdict
import re
import queue
import random


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



def gan(s):
  return map(int, re.findall(r'-?\d+', s))


def lenr(l):
  return range(len(l))


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
input = '''pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<10,10,10>, r=5'''
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
# result = solve(input)
# print("Result: {}".format(result))

nanobots = input


def dist(p1, p2):
  (x0, y0, z0) = p1
  (x1, y1, z1) = p2
  return abs(x0-x1) + abs(y0-y1) + abs(z0-z1)


srad = 0
rad_idx = 0
in_range = defaultdict(int)
for i in lenr(nanobots):
  pos, rng = nanobots[i]
  strength = 0
  if rng > srad:
    srad = rng
    rad_idx = i
    for j in lenr(nanobots):
      npos, _ = nanobots[j]
      if dist(pos, npos) <= rng:
        in_range[i] += 1

print("a", in_range[rad_idx])


def zabs(x):
  return If(x >= 0, x, -x)


(x, y, z) = (Int('x'), Int('y'), Int('z'))
in_ranges = [
    Int('in_range_' + str(i)) for i in lenr(nanobots)
]
range_count = Int('sum')
o = Optimize()
for i in lenr(nanobots):
  (nx, ny, nz), nrng = nanobots[i]
  o.add(in_ranges[i] == If(zabs(x - nx) +
        zabs(y - ny) + zabs(z - nz) <= nrng, 1, 0))
o.add(range_count == sum(in_ranges))
dist_from_zero = Int('dist')
o.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
h1 = o.maximize(range_count)
h2 = o.minimize(dist_from_zero)
print(o.check())
# print o.lower(h1)
# print o.upper(h1)
print("b", o.lower(h2), o.upper(h2))
# print o.model()[x]
# print o.model()[y]
# print o.model()[z]
