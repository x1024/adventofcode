import queue
import collections

offsets = [
  (1, 0, 0),
  (-1, 0, 0),
  (0, 1, 0),
  (0, -1, 0),
  (0, 0, 1),
  (0, 0, -1),
]

MIN, MAX = 0, 20
LAVA = 0
AIR_POCKET = 1
EMPTY = 2
TMP = 3


def mark_air_pockets(start, _map):
  if start in _map: return
  q = queue.Queue()
  q.put(start)
  is_outside = False

  while not q.empty():
    cube = q.get()
    if cube in _map: continue
    _map[cube] = TMP
    if all(MIN < c < MAX for c in cube):
      for offset in offsets: q.put(tuple(map(sum, zip(cube, offset))))
    else:
      is_outside = True

  tile_type = EMPTY if is_outside else AIR_POCKET
  _map.update((c, tile_type) for c, v in _map.items() if v == TMP)


def empty_sides(c, _map):
  return sum(_map[tuple(map(sum, zip(c, o)))] == EMPTY for o in offsets)


def solve(lava, exclude_air_pockets=False):
  _map = collections.defaultdict(lambda: EMPTY, [(c, LAVA) for c in lava])

  if exclude_air_pockets:
    for c in lava:
      for o in offsets:
        mark_air_pockets(tuple(map(sum, zip(c, o))), _map)

  return sum(empty_sides(cube, _map) for cube in lava)


def parse_input(input):
  return set(tuple(map(int, row.split(','))) for row in input.split("\n"))


def test():
  input = '''
1,2,2
1,2,5
2,1,2
2,1,5
2,2,1
2,2,2
2,2,3
2,2,4
2,2,6
2,3,2
2,3,5
3,2,2
3,2,5
  '''

  input = parse_input(input)
  print(solve(input))
  print(solve(input, exclude_air_pockets=True))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
print(solve(input))
print(solve(input, exclude_air_pockets=True))
