import z3
from z3 import *


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

    o.check()
    m = o.model()
    
    return (sum([m.eval(p).as_long() for p in rock_pos]))


data_test = open('input-sample.txt', 'r').read().strip()
# result = main(data_test, part2=True)
result = main(data_test)
print("Test Result: {}".format(result))

# exit()

data = open('input.txt', 'r').read().strip()
result = main(data, LIM=10000, _min=200000000000000, _max=400000000000000)
print("Real Result: {}".format(result))
