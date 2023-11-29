import functools
import pprint
import queue
import re
import pyparsing as pp

thecontent = pp.Literal("N") | pp.Literal("W") | pp.Literal("S") | pp.Literal("E") | pp.Literal('|').suppress()
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
    # for p in positions: rooms.add(p)
    for item in regex:
      # print(item, type(item))
      new_positions = []

      if type(item) == str:
        for pos in positions:
          new_pos = pos + offsets[item]
          rooms.add(new_pos)
          doors.add((pos, new_pos))
          new_positions.append(new_pos)
      else:
        for p in solve_part(item, positions):
          new_positions.append(p)
      print(item, regex)
      print_floor(rooms, doors)

      positions = tuple(new_positions)
    return positions

  start = 0 + 0j
  rooms.add(start)
  print(parse_regex(regex))
  solve_part(parse_regex(regex), (start,))
  # print(rooms)
  # print(doors)
  print_floor(rooms, doors)

  q = queue.Queue()
  q.put((start, 0))
  seen = set()
  max_steps = 0
  while not q.empty():
    pos, steps = q.get()
    max_steps = max(max_steps, steps)
    # print(pos, steps)
    if pos in seen: continue
    seen.add(pos)
    for o in offsets.values():
      new_pos = pos + o
      if (pos, new_pos) in doors:
        q.put((new_pos, steps + 1))
  return max_steps

  # return rooms, doors


def print_floor(rooms, doors):
  minx = int(min(room.real for room in rooms))
  maxx = int(max(room.real for room in rooms))
  miny = int(min(room.imag for room in rooms))
  maxy = int(max(room.imag for room in rooms))
  dx = maxx - minx + 1
  dy = maxy - miny + 1
  data = []
  for _ in range(dx * 2 + 1):
    data.append(['#'] * (dy * 2 + 1))
  for room in rooms:
    x, y = int(room.real) - minx, int(room.imag) - miny
    x, y = x * 2 + 1, y * 2 + 1
    # print('asd', x, y, len(data), len(data[0]))
    data[x][y] = '.'

  for door in doors:
    d1, d2 = door
    x1, y1 = int(d1.real) - minx, int(d1.imag) - miny
    x1, y1 = x1 * 2 + 1, y1 * 2 + 1
    x2, y2 = int(d2.real) - minx, int(d2.imag) - miny
    x2, y2 = x2 * 2 + 1, y2 * 2 + 1
    x, y = (x1 + x2) // 2, (y1 + y2) // 2
    # print(x, y, dx * 2, dy * 2)
    data[x][y] = '|'
  data[(0 - minx) * 2 + 1][(0 - miny) * 2 + 1] = 'X'
  print('\n'.join(''.join(row) for row in data))
  print("-------")


def to_tuple(lst):
  if type(lst) == list:
    return tuple(map(to_tuple, lst))
  return lst

def parse_regex(regex):
  regex = (regex
    .replace("^", "(")
    .replace("$", ")")
  )
  result = parens.parseString(regex).asList()[0]
  return to_tuple(result)


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
  # assert solve("^WNENNN$") == 6
  assert solve("^ENWWW(NEEE|SSE(EE|N))$") == 10
  # assert solve("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$") == 18
  exit()


test()
data = open('input.txt', 'r').read().strip()
result = solve(data)
print("Result: {}".format(result))
