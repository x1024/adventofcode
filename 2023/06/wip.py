import numpy
import re
import math


def solve(time, distance):
    # i^2 - time * i + (distance + 1) <= 0
    roots = numpy.roots([1, -time, distance + 1])
    return math.floor(roots[0]) - math.ceil(roots[1]) + 1


data = [list(map(int, row.split())) for row in re.sub("[^\d \n]", "", open('input.txt', 'r').read()).split('\n')[:-1]]
print(math.prod(solve(*row) for row in zip(*data)))
print(solve(*[int("".join(map(str, row))) for row in data]))
