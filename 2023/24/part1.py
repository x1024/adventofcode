import collections
import numpy
import pprint
import re
import functools
import itertools


def det(a, b): return a[0] * b[1] - a[1] * b[0]


def line_intersection(point1, point2):
    pos1, vel1 = point1
    pos2, vel2 = point2
    line1 = (pos1, tuple(map(sum, zip(pos1, vel1))))
    line2 = (pos2, tuple(map(sum, zip(pos2, vel2))))

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)
    if div == 0: return tuple()

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    time1 = (x - line1[0][0]) / (line1[1][0] - line1[0][0])
    time2 = (x - line2[0][0]) / (line2[1][0] - line2[0][0])
    if time1 < 0: return tuple()
    if time2 < 0: return tuple()
    return (x, y)


def main(data, MIN, MAX):
    points = []
    for row in data.split('\n'):
        pos, vel = row.split("@")
        pos = list(map(int, pos.split(",")))
        vel = list(map(int, vel.split(",")))
        points.append((pos, vel))

    part1 = sum(sum(MIN <= i <= MAX for i in line_intersection(p1, p2)) == 2
        for p1, p2 in itertools.combinations(points, 2))

    return (res)


data = open('input-sample.txt', 'r').read().strip()
print(main(data, 7, 27))

data = open('input.txt', 'r').read().strip()
print(main(data, 200000000000000, 400000000000000))
