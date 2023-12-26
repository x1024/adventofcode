#!/usr/bin/env python3

# from utils.all import *

# https://stackoverflow.com/a/20677983/3889449
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None, None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


data = open('input.txt', 'r').read().strip()
lines = data.split("\n")
stuff = []

for row in lines:
    pos, vel = row.split("@")
    pos = list(map(int, pos.split(",")))
    vel = list(map(int, vel.split(",")))
    stuff.append((pos, vel))

import z3

# BitVec is way faster than Int
I = lambda name: z3.BitVec(name, 64)

x, y, z = I('x'), I('y'), I('z')
vx, vy, vz = I('vx'), I('vy'), I('vz')

s = z3.Solver()

for i, a in enumerate(stuff):
    print(a)
    (ax, ay, az), (vax, vay, vaz) = a

    t = I(f't_{i}')
    s.add(t >= 0)
    s.add(x + vx * t == ax + vax * t)
    s.add(y + vy * t == ay + vay * t)
    s.add(z + vz * t == az + vaz * t)

assert s.check() == z3.sat

m = s.model()
x, y, z = m.eval(x), m.eval(y), m.eval(z)
x, y, z = x.as_long(), y.as_long(), z.as_long()

ans2 = x + y + z
print(ans2)
