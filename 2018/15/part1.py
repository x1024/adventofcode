import collections
import pprint
import queue
import numpy
import time

DEAD = 'D'
GNOME = 'G'
ELF = 'E'
EMPTY = '.'
OFFSETS = [
  # Order matters
  (-1,  0),
  ( 0, -1),
  ( 0, +1),
  (+1,  0),
]
MOVE = 0
FIGHT = 1
STAY = 2
INITIAL_HP = 200
ATT = 3

def opposite_type(target_type):
  if target_type == GNOME:
    return ELF
  else:
    return GNOME

def solve(data):
  n, m = len(data), len(data[0])

  def check_empty(p):
    x, y = p
    if x < 0 or x >= n or y < 0 or y >= m:
      return False
    return data[x][y] == '.'

  def get_pieces(target_type):
    result = []
    for x in range(n):
      row = data[x]
      for y in range(m):
        cell = row[y]
        if cell == target_type:
          result.append((x, y))
    return result

  def get_targets(target_type):
    result = []
    for x in range(n):
      row = data[x]
      for y in range(m):
        cell = row[y]
        if cell != target_type:
          continue
        for (dx, dy) in OFFSETS:
          p = x + dx, y + dy
          if check_empty(p):
            # print (x1, y1)
            result.append(p)
    return list(sorted(result))
  
  def calculate_paths(start, tgts):
    paths = {}
    tgts = set(tgts)
    q = queue.Queue()
    q.put(start)
    while not q.empty():
      x, y = q.get()
      for (dx, dy) in OFFSETS:
        x1, y1 = x + dx, y + dy
        p = (x1, y1)
        if not check_empty(p): continue
        if p in paths: continue
        paths[p] = (x, y)
        q.put(p)

    routes = {}
    for tgt in tgts:
      route = []
      if not tgt in paths: continue
      routes[tgt] = route
      while tgt != start:
        route.append(tgt)
        tgt = paths[tgt]
    return routes.values()

  def bfs(start, end):
    q = queue.Queue()
    q.put(start)
    dist = {}
    dist[start] = 0
    while not q.empty():
      pos = q.get()
      x, y = pos
      if pos == end: continue
      for (dx, dy) in OFFSETS:
        p = (x + dx, y + dy)
        if p in dist: continue
        if p != end and not check_empty(p): continue
        dist[p] = dist[pos] + 1
        q.put(p)

    x, y = end
    results = []
    for (dx, dy) in OFFSETS:
      p = (x + dx, y + dy)
      if not check_empty(p): continue
      d = dist.get(p, None)
      if d is None: continue
      results.append((d, p))

    # print("----")
    # print(results)
    # print(start, end)
    # pprint.pprint(dist)
    # print("----")
    return min(results)[1]


  def get_move(piece):
    x, y, piece_type = piece
    opp = opposite_type(type)
    tgts = get_targets(opp)
    pos = (x, y)
    # print(pos, piece_type, tgts)
    if pos in tgts:
      return (FIGHT, (-1, -1))
    for (dx, dy) in OFFSETS:
      x1, y1 = x + dx, y + dy
      if x1 < 0 or x1 >= n or y1 < 0 or y1 >= m: continue
      if data[x1][y1] == opp:
        return (FIGHT, (-1, -1))
    paths = calculate_paths(pos, tgts)
    if not paths:
      return (STAY, (-1, -1))

    min_len = min(len(p) for p in paths)
    paths = [p[::-1] for p in paths if len(p) == min_len]
    best_path = min(paths)
    target = best_path[-1]
    # print("!!!!", piece_type, target, pos, best_path, bfs(target, pos))
    assert best_path[0] == bfs(target, pos)
    # exit()
    return (MOVE, best_path[0])

  hp = {}
  for x in range(n):
    row = data[x]
    for y in range(m):
      cell = row[y]
      if cell == 'G' or cell == 'E':
        hp[(x, y)] = INITIAL_HP

  # for row in data: print(''.join(row))
  # input()

  moves = 0
  while True:
    pieces = []
    for x in range(n):
      row = data[x]
      for y in range(m):
        cell = row[y]
        if cell == 'G' or cell == 'E':
          pieces.append([x, y, cell])

    new_pieces = []
    for i in range(len(pieces)):
      piece = pieces[i]
      # move
      x, y, type = piece
      # print(piece)
      if type == DEAD:
        # print("Just Killed")
        continue # just killed

      opp = opposite_type(type)
      if not get_pieces(opp):
        # print(opp, get_pieces(opp))
        # print(moves, sum(hp.values()), hp.values())

        # print(moves)
        # for key in sorted(hp): print(data[key[0]][key[1]], key, hp[key])
        # for row in data: print(''.join(row))

        return moves * sum(hp.values())

      action, pos = get_move(piece)
      if action == MOVE:
        data[x][y] = EMPTY
        data[pos[0]][pos[1]] = type
        h = hp[(x, y)]
        del hp[(x, y)]
        hp[pos] = h
        x, y = pos
      new_pieces.append((pos[0], pos[1], type))

      # attack
      tgts = []
      for (dx, dy) in OFFSETS:
        x1, y1 = x + dx, y + dy
        if x1 < 0 or x1 >= n or y1 < 0 or y1 >= m: continue
        if data[x1][y1] == opp:
          tgts.append((hp[(x1, y1)], (x1, y1)))
      if not tgts: continue
      tgts = list(sorted(tgts))
      target = tgts[0]
      t_pos = target[1]
      hp[t_pos] -= 3
      if hp[t_pos] <= 0:
        del hp[t_pos]
        data[t_pos[0]][t_pos[1]] = '.'
        for j in range(len(pieces)):
          p = pieces[j]
          if p[0] == t_pos[0] and p[1] == t_pos[1]:
            p[2] = DEAD
            break

    moves += 1
    # print("")
    # print("")
    # print("")
    # print(moves)
    # for key in sorted(hp):
    #   if key[0] in [18, 19, 20, 21]:
    #     print(data[key[0]][key[1]], key, hp[key])
    for row in data: print(''.join(row))
    # input()
    # time.sleep(2)

  return 0


def parse_line(data):
  return list(data)


def parse_data(data):
  data = data.split('\n')
  data = [row.strip() for row in data]
  data = [row for row in data if row]
  # data = list(map(int, data))
  data = list(map(parse_line, data))
  return data


def test():
  data = '''
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
'''
  solve(parse_data(data))

  data = '''
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
'''
  assert solve(parse_data(data)) == 27730

  data = '''
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
'''
  assert solve(parse_data(data)) == 36334

  data = '''
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
'''
  assert solve(parse_data(data)) == 39514

  data = '''
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
'''
  assert solve(parse_data(data)) == 27755

  data = '''
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
'''
  assert solve(parse_data(data)) == 28944

  data = '''
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
'''
  assert solve(parse_data(data)) == 18740

  return



# test()
data = open('input.txt', 'r').read().strip()
data = parse_data(data)
result = solve(data)
print("Result: {}".format(result))
