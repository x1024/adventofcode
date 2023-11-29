import functools
import json
import pprint
import queue
import re
import pyparsing as pp

thecontent = pp.Word("NWSE") | pp.Literal('|').suppress()
parens = pp.nestedExpr('(', ')', content=thecontent)


offsets = {
  'N': -1 + 0j,
  'W':  0 - 1j,
  'S': +1 + 0j,
  'E':  0 + 1j,
}


def solve(regex):
  rooms = set()
  doors = set()

  @functools.cache
  def solve_part(regex, positions):
    # print(len(regex), len(positions), len(rooms))
    # for p in positions: rooms.add(p)
    for item in regex:

      if type(item) == str:
        new_positions = []
        for pos in positions:
          new_pos = pos + offsets[item]
          rooms.add(new_pos)
          doors.add((pos, new_pos))
          new_positions.append(new_pos)
      else:
        new_positions = []
        for part in item:
          for p in solve_part(part, positions):
            new_positions.append(p)

      positions = tuple(set(new_positions))
    return positions

  start = 0 + 0j
  rooms.add(start)
  solve_part(parse_regex(regex), (start,))
  print_floor(rooms, doors)

  res = []
  q = queue.Queue()
  q.put((start, 0))
  seen = set()
  max_steps = 0
  while not q.empty():
    pos, steps = q.get()
    if pos in seen: continue
    max_steps = max(max_steps, steps)
    if steps >= 1000: res.append(pos)
    print(pos, steps, max_steps)
    seen.add(pos)
    for o in offsets.values():
      new_pos = pos + o
      if (pos, new_pos) in doors:
        q.put((new_pos, steps + 1))
  return max_steps, len(res)


  # return rooms, doors


def print_floor(rooms, doors):
  minx = int(min(room.real for room in rooms))
  maxx = int(max(room.real for room in rooms))
  miny = int(min(room.imag for room in rooms))
  maxy = int(max(room.imag for room in rooms))
  dx = maxx - minx + 1
  dy = maxy - miny + 1
  data = []
  for _ in range(dy * 2 + 1):
    data.append(['#'] * (dx * 2 + 1))
  for room in rooms:
    x, y = int(room.real) - minx, int(room.imag) - miny
    x, y = x * 2 + 1, y * 2 + 1
    data[x][y] = '.'

  for door in doors:
    d1, d2 = door
    x1, y1 = int(d1.real) - minx, int(d1.imag) - miny
    x1, y1 = x1 * 2 + 1, y1 * 2 + 1
    x2, y2 = int(d2.real) - minx, int(d2.imag) - miny
    x2, y2 = x2 * 2 + 1, y2 * 2 + 1
    x, y = (x1 + x2) // 2, (y1 + y2) // 2
    data[x][y] = '|' if x1 == x2 else '-'
  data[(0 - minx) * 2 + 1][(0 - miny) * 2 + 1] = 'X'
  print('\n'.join(''.join(row) for row in data))


def to_tuple(lst):
  if type(lst) == list:
    return tuple(map(to_tuple, lst))
  return lst


def parse_regex(regex):
  regex = (regex
    .replace("(", "[[")
    .replace(")", "]],")
    .replace("|", "],[")
    .replace("N", '"N",')
    .replace("W", '"W",')
    .replace("E", '"E",')
    .replace("S", '"S",')
    .replace("^", "[")
    .replace("$", "]")
    .replace(",]", "]")
  )

  return to_tuple(json.loads(regex))


def test():
  input = '''
#####
#.|.#
#-###
#.|X#
#####
  '''.strip("\n")
  # input = parse_input(input)
  # assert solve("^WNE$") == 3
  # assert solve("^ENWWW(NEEE|SSE(EE|N))$") == 10
  # assert solve("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$") == 18
  assert solve("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$") == 31
  exit()


# test()
data = open('input.txt', 'r').read().strip()
result = solve(data)
print("Result: {}".format(result))
