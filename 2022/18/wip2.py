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

LAVA = 0
AIR_POCKET = 1
EMPTY = 2
TMP = -1

def solve(lava):
  MIN = min(min(c) for c in lava)
  MAX = max(max(c) for c in lava)
  _map = collections.defaultdict(lambda: EMPTY)
  _map.update((c, LAVA) for c in lava)

  def bfs(start):
    if start in _map: return
    current_group = set()
    q = queue.Queue()
    q.put(start)
    is_outside = False
    while not q.empty():
      cube = q.get()
      if cube in _map: continue
      _map[cube] = TMP
      current_group.add(cube)
      if any(c < MIN or c > MAX for c in cube):
        is_outside = True
        continue

      for offset in offsets:
        new_cube = cube[0] + offset[0], cube[1] + offset[1], cube[2] + offset[2]
        q.put(new_cube)

    for c in current_group:
      _map[c] = EMPTY if is_outside else AIR_POCKET

  for x in range(MIN, MAX + 1):
    for y in range(MIN, MAX + 1):
      for z in range(MIN, MAX + 1):
        if (x == MIN or x == MAX or y == MIN or y == MAX or z == MIN or z == MAX) and (x, y, z) in lava:
          print((x, y, z, MIN, MAX))
        bfs((x, y, z))

  def empty_sides(c):
    return sum(_map[c[0] + o[0], c[1] + o[1], c[2] + o[2]] == EMPTY for o in offsets)

  minx = min(c[0] for c in lava)
  maxx = max(c[0] for c in lava)
  miny = min(c[1] for c in lava)
  maxy = max(c[1] for c in lava)
  minz = min(c[2] for c in lava)
  maxz = max(c[2] for c in lava)

  sides = []

  for z in [minz, maxz]:
    side = []
    for x in range(minx, maxx + 1):
      line = []
      for y in range(miny, maxy + 1):
        char = ' '
        if _map[(x, y, z)] == LAVA:
          char = '#'
        line.append(char)
      side.append(''.join(line))

    sides.append(side)

  for y in [miny, maxy]:
    side = []
    for x in range(minx, maxx + 1):
      line = []
      for z in range(minz, maxz + 1):
        char = ' '
        if _map[(x, y, z)] == LAVA:
          char = '#'
        if _map[(x, y, z)] == AIR_POCKET:
          char = 'o'
        line.append(char)
      side.append(''.join(line))
    sides.append(side)

  for x in [minx, maxx]:
    side = []
    for y in range(miny, maxy + 1):
      line = []
      for z in range(minz, maxz + 1):
        char = ' '
        if _map[(x, y, z)] == LAVA:
          char = '#'
        line.append(char)
      side.append(''.join(line))
    sides.append(side)

  for row in zip(*sides):
    print(' | '.join(row))
  # for side in sides:
    # for row in side:
      # print(row)
      # print(' | '.join(row))

      # for z in range(minz, maxz + 1):
        # if _map[x, y, z] == LAVA:
          # if empty_sides((x, y, z)) >= 2:
            # return True

  return sum(empty_sides(cube) for cube in lava)


def parse_line(input):
  return tuple(map(int, input.split(',')))


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  input = list(map(parse_line, input))
  input = set(input)
  return input


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
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

