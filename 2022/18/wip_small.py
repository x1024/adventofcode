import sys
lava = set(tuple(map(int, row.split(','))) for row in open('input.txt', 'r').read().strip().split("\n"))
OUTSIDE, INSIDE, MIN, MAX = True, False, min(min(l) for l in lava), max(max(l) for l in lava)
sys.setrecursionlimit((MAX - MIN + 4)**3)
def sides(x, y, z): return ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1))
def mark_outside(cube, _map = dict((c, False) for c in lava)):
  _map[cube] = _map.get(cube, OUTSIDE)
  return next(iter([mark_outside(side) for side in sides(*cube) if not side in _map and all(MIN - 1 <= c <= MAX + 1 for c in cube)]), _map)
print(sum(mark_outside((MIN, MIN, MIN)).get(side, OUTSIDE) == OUTSIDE for side in sum((sides(*cube) for cube in lava), tuple())))
print(sum(mark_outside((MIN, MIN, MIN)).get(side, INSIDE) == OUTSIDE for side in sum((sides(*cube) for cube in lava), tuple())))