import collections
import numpy
import pprint
import re
import functools
import itertools
import math

import shapely
from shapely.geometry import LineString, Point

import z3
from z3 import *



def line_intersection(line1, line2, c1=0, c2=1):
    # print(line1[0])
    # print(line1[1])
    print('qwe', line1, line2)
    xdiff = (line1[0][c1] - line1[1][c1], line2[0][c1] - line2[1][c1])
    ydiff = (line1[0][c2] - line1[1][c2], line2[0][c2] - line2[1][c2])
    # print(line1, line2)
    print("\t", xdiff, ydiff)

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        print("parallel")
        return None
        # raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    for c in (c1, c2):
        d1 = (line1[1][c1] - line1[0][c1])
        if d1 != 0:
            time1 = (x - line1[0][c1]) / d1
            if time1 < 0: return None
        d2 = (line2[1][c1] - line2[0][c1])
        if d2 != 0:
            time2 = (x - line2[0][c1]) / d2
            if time2 < 0: return None
    # print((x, y), time1, time2)
    return (x, y)

def get_coords(line, coords):
    pos, vel = line
    pos = tuple(pos[c] for c in coords)
    vel = tuple(vel[c] for c in coords)
    return pos, vel

def line_intersection_3d(line1, line2, coords = ((0, 1), (0, 2), (1, 2))):
    print(line1, line2)
    print("--->")

    intersect = [
        line_intersection(
            get_coords(line1, coord),
            get_coords(line2, coord)
        )
        for coord in coords
    ]
    print(intersect)
    print("--->")

    if any(not i for i in intersect): return None
    if not all(i == intersect[0] for i in intersect): return None
    return intersect[0]


def intersection_time(line1, line2):
    pos1, vel1 = line1
    pos2, vel2 = line2
    dx = pos2[0] - pos1[0]
    dp = [pos2[i] - pos1[i] for i in range(3)]
    dv = [vel2[i] - vel1[i] for i in range(3)]

    ts = []
    for i in range(len(dv)):
        if dv[i] == 0:
            if dp[i] != 0: return None
        else:
            if dp[i] % dv[i] != 0: return None
            t = -dp[i] / dv[i]
            ts.append(t)
    if all(t == ts[0] for t in ts): return ts[0]
    return None


def main(data, LIM=10, _min=7, _max=27):
    data = [row.strip() for row in data.split('\n')]

    points = []
    for row in data:
        pos, vel = row.split("@")
        pos = list(map(int, pos.split(",")))
        vel = list(map(int, vel.split(",")))
        points.append((pos, vel))

    o = Solver()

    rock_pos = Int("x"), Int("y"), Int("z")
    rock_vel = Int("vx"), Int("vy"), Int("vz")
    rock = rock_pos, rock_vel

    coords = (0, 1, 2)

    for i, (pos, vel) in enumerate(points):
        t = Int("t_%s" % i)
        o.add(t > 0)
        for c in coords:
            o.add(rock_pos[c] + rock_vel[c] * t == pos[c] + vel[c] * t)

    print(o.check())
    m = o.model()
    
    print([m.eval(p).as_long() for p in rock_pos])
    print(sum([m.eval(p).as_long() for p in rock_pos]))
    return (sum([m.eval(p).as_long() for p in rock_pos]))

    exit()

    for dt in [5]:
        # p(t) == pos1(t)
        # p(t+dt) == pos2(t + dt)

        pos2 = point(p2, dt)
        _p2 = (pos2, vel2)

        print("AD")
        print(tuple(dpos[i] - dvel[i] * dt for i in range(len(pos1))))
        print("AD")

        print(point(p1, 3), point(_p2, 3))
        print(dt, pos2, intersection_time(p1, _p2))
    exit()
    print(intersection_time(p1, p2))
    print(i, j)
    print(dpos, dvel)
    g = math.gcd(*dvel)
    dvel = tuple(i // g for i in dvel )
    print(dpos, dvel, g)
    exit()
    for c in (0, 1, 2):
        points2 = [
            (pos[c], vel[c]) for pos, vel in points
        ]

    for c in (0, 1, 2):
        points2 = [
            (pos[c], vel[c]) for pos, vel in points
        ]

        # print(points2)
        valid = {}
        for i in options:
            pos, vel = points2[i]
            def check(dx):
                start = (pos + vel) - dx
                rock = (start, dx)
                return all(collision_good(rock, point) for point in points2)

            # print(i)
            # dx = binsearch(lambda dx: check(dx - LIM), LIM * 2)
            # print(i, dx)
            for dx in range(-LIM, LIM):
                if check(dx):
                    # valid.append((i, dx))
                    valid[i] = dx
                    print("MAY BE", c, dx)
                    # print(list(collision_time(rock, point) for point in points2))
                # print(len(times))
        options = valid.keys()
        res.append(valid)

    print(res)
    for k in res[0]:
        if not (k in res[1] and k in res[2]): continue
        pos1, vel1 = points[k]
        vel = res[0][k], res[1][k], res[2][k]
        pos = tuple(pos1[i] + vel1[i] - vel[i] for i in range(3))
        print(pos)
        print(sum(pos))
        return sum(pos)
    # print(res)



data_test = open('input-sample.txt', 'r').read().strip()
# result = main(data_test, part2=True)
result = main(data_test)
print("Test Result: {}".format(result))

# exit()

data = open('input.txt', 'r').read().strip()
result = main(data, LIM=10000, _min=200000000000000, _max=400000000000000)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
