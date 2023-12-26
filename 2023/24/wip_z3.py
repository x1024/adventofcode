import z3
import itertools
from z3 import *


def main(data, MIN, MAX):
    T = Real
    data = [row.strip() for row in data.split('\n')]

    points = []
    for row in data:
        pos, vel = row.split("@")
        pos = tuple(map(int, pos.split(",")))
        vel = tuple(map(int, vel.split(",")))
        points.append((pos, vel))

    def solve(points):
        (p1, v1), (p2, v2) = points
        o = Solver()
        t1 = T("t1")
        t2 = T("t2")
        o.add(t1 > 0)
        o.add(t2 > 0)
        for c in (0, 1):
            o.add(p1[c] + v1[c] * t1 == p2[c] + v2[c] * t2)
            o.add(p1[c] + v1[c] * t1 >= MIN)
            o.add(p1[c] + v1[c] * t1 <= MAX)
        return o.check() == sat

    part1 = sum(map(solve, itertools.combinations(points, 2)))

    T = Real
    o = Solver()
    rock_pos = T("x"), T("y"), T("z")
    rock_vel = T("vx"), T("vy"), T("vz")

    coords = (0, 1, 2)
    for i, (pos, vel) in enumerate(points):
        t = T("t_%s" % i)
        o.add(t > 0)
        for c in coords:
            o.add(rock_pos[c] + rock_vel[c] * t == pos[c] + vel[c] * t)

    o.check()
    m = o.model()
    
    part2 = (sum([m.eval(p).as_long() for p in rock_pos]))

    return part1, part2


data_test = open('input-sample.txt', 'r').read().strip()
print(main(data_test, 7, 27))

# exit()

data = open('input.txt', 'r').read().strip()
print(main(data, 200000000000000, 400000000000000))
