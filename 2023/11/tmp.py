import itertools
import numpy as np

def solve_axis(rows, scale):
    empty_rows = np.cumsum(['#' not in row for row in rows])
    stars = [(x + (scale - 1) * empty_rows[x], str(rows[x]).count('#')) for x in range(len(rows))]
    return sum(ca * cb * abs(a - b) for ((a, ca), (b, cb)) in itertools.combinations(stars, 2))

def solve(rows, scale): return solve_axis(rows, scale) + solve_axis(np.rot90(np.array(rows), -1), scale)

data = np.array([list(row) for row in open('input.txt', 'r').read().strip().split('\n')])
print(solve(data, 2))
print(solve(data, 10**6))
