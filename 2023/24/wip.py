import z3
import itertools
import numpy as np


def det(a, b): return int(a[0]) * int(b[1]) - int(a[1]) * int(b[0])
def ray_time(ray, point): return min((pt - p) / v for p, v, pt in zip(*ray, point) if v != 0)


def intersect(ray1, ray2):
    (pos1, vel1), (pos2, vel2) = (ray1, ray2)

    xdiff = (vel1[0], vel2[0])
    ydiff = (vel1[1], vel2[1])

    div = -det(xdiff, ydiff)
    if div == 0: return None

    d = det(pos1, pos1 + vel1), det(pos2, pos2 + vel2)
    pt = det(d, xdiff) / div, det(d, ydiff) / div
    return pt


def is_valid_intersection(rays, bounds):
    pt = intersect(rays[0], rays[1])
    if pt is None: return False
    if not all(bounds[0] <= i <= bounds[1] for i in pt): return False
    if not all(ray_time(ray, pt) > 0 for ray in rays): return False
    return True


def main_z3(data, bounds, LIM):
    rays = [tuple(np.array(tuple(map(int, s.split(",")))) for s in row.split("@")) for row in data.split("\n")]
    part1 = sum(is_valid_intersection(rays, bounds) for rays in itertools.combinations(rays, 2))

    T = z3.Real
    o = z3.Solver()
    rock = (T("x"), T("y"), T("z")), (T("vx"), T("vy"), T("vz"))
    for i, ray in enumerate(rays):
        t = T("t_%s" % i)
        o.add(t > 0)
        o.add([rp + rv * t == p + v * t for rp, rv, p,v in zip(*rock, *ray)])
    o.check()
    part2 = (sum([o.model().eval(p).as_long() for p in rock[0]]))

    return part1, part2


def main(data, bounds, LIM):
    rays = [tuple(np.array(tuple(map(int, s.split(",")))) for s in row.split("@")) for row in data.split("\n")]
    part1 = sum(is_valid_intersection(rays, bounds) for rays in itertools.combinations(rays, 2))

    for vel_xy in itertools.product(range(-LIM, LIM), repeat=2):
        a, b, *rest = [(pos[:2], (vel[:2] - vel_xy)) for pos, vel in rays]
        pos_xy = intersect(a, b)
        if pos_xy is not None and all(intersect(a, r) == pos_xy for r in rest): break
    for vel_z in range(-LIM, LIM):
        a, b, *rest = [(pos[1:], (vel[1:] - (vel_xy[1], vel_z))) for pos, vel in rays]
        pos_yz = intersect(a, b)
        if pos_yz is not None and all(intersect(a, r) == pos_yz for r in rest): break
    part2 = int(sum(pos_xy + pos_yz[1:]))

    return part1, part2


data, bounds, limit = open('input-sample.txt', 'r').read().strip(), (7, 27), 10
print(main_z3(data, bounds, limit))
print(main(data, bounds, limit))

data, bounds, limit = open('input.txt', 'r').read().strip(), (200000000000000, 400000000000000), 290
print(main_z3(data, bounds, limit))
print(main(data, bounds, limit))
