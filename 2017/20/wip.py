def move(point, steps):
    pos, vel, acc = point
    return tuple(pos[i] + vel[i] * steps + acc[i] * steps * (steps + 1) / 2
                 for i in range(3))

COLLISION_ALWAYS = 'ALWAYS'

def collision_3(pa, pb):
  cs = [
    collision(tuple(_[i] for _ in pa), tuple(_[i] for _ in pb))
    for i in range(3)
  ]
  cs = [c for c in cs if c != COLLISION_ALWAYS]
  if len(set(cs)) != 1:
    return -1
  return cs[0]


def collision(pa, pb):
    p0, v0, a0 = pa
    p1, v1, a1 = pb

    if pa == pb:
      return COLLISION_ALWAYS
    # print(pa, pb)

    # s = p + v*s + a*s*(s+1)/2
    # s1 = s2

    # p0 + v0*s + a0*s*(s+1)/2 = p1 + v1*s + a1*s*(s+1)/2
    # 2*(p0 - p1) + s*2*(v0-v1) + (s ^ 2 + s) * (a0-a1) = 0
    # s ^ 2 * (a0-a1) + s * (2*(v0-v1) + (a0-a1)) + 2*(p0-p1) = 0

    a = (a0-a1)
    if a == 0:
      # s = p + v*s + a*s*(s+1)/2
      # s1 = s2
      # p0 + v0*s = p1 + v1*s
      if v0 == v1:
        if p0 == p1:
          return 0
        return -1
      s = (p1 - p0) / (v0 - v1)
      return s
    else:
      b = (2*(v0-v1) + (a0-a1))
      c = 2*(p0 - p1)
      # print("ads", a, b, c)
      D = b*b - 4*a*c
      if D < 0:
        return -1
      s1 = (-b + (D) ** 0.5) / (2*a)
      s2 = (-b - (D) ** 0.5) / (2*a)
      # print(s1, s2)
      if s1 < 0: return s2
      if s2 < 0: return s1
      return min(s1, s2)


import pprint
import collections

def coll(pa, pb, steps = 0):
  while True:
    ma = move(pa, steps)
    mb = move(pb, steps)
    dx = (
      ma[0] - mb[0],
      ma[1] - mb[1],
      ma[2] - mb[2]
    )
    dist = sum(abs(_) for _ in dx)
    if dist == 0:
      return steps
    if dist > 10000:
      return -1
    steps += 1

def solve(points):
  steps = 0
  l = len(points)
  cols = {}
  for i in range(l):
    print(i)
    for j in range(i+1, l):
      c = coll(points[i], points[j])
      cols[(i, j)] = c
  used = set()

  while True:
    l = len(points)
    remaining = [v for k, v in cols.items() if k[0] not in used and k[1] not in used and v >= 0]
    if not remaining:
      break
    steps = min(remaining)
    print(steps)
    for i in range(l):
      if i in used: continue
      for j in range(i+1, l):
        if j in used: continue
        if cols[(i, j)] == steps:
          used.add(i)
          used.add(j)

    print(len(points), len(used), len(points) - len(used))

  print(len(points), len(used))
  return len(points) - len(used)
  exit()
  seen = {}
  for p in points:
    seen[p[0]] = seen.get(p[0], 0) + 1
  points = [p for p in points if seen[p[0]] < 2]
  print(steps, len(points))

  steps += 1
  points = [
    (move(p, 1), p[1], p[2])
    for p in points
  ]

  # pprint.pprint(points)
  return len(points)


def solve_easy(points):
    # smallest accelleration wins
    points = [sum(map(abs, row[2])) for row in points]
    best_index = 0
    for i, row in enumerate(points):
        if row < points[best_index]:
            best_index = i
    return best_index


def parse_line(input):
    return tuple(map(parse_tuple, input.split(", ")))


def parse_tuple(input):
    return tuple( int(i) for i in input[3:-1].split(',') )


def binsearch(pred, lim=2**20):
    cur = 0
    while lim > 0:
        cur += pred(cur + lim) * lim
        lim >>= 1
    return cur


def parse_input(input):
    input = input.split('\n')
    input = [row.strip() for row in input]
    input = [row for row in input if row]
    # input = map(int, input)
    input = list(map(parse_line, input))
    return input


def test():
  input = '''
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
'''
  input = parse_input(input)
  # result = solve_easy(input)
  # print("Test Result: {}".format(result))
  # assert result == 0


  input = '''
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
  '''

  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  assert result == 1

  '''
  p = ((0, 0, 0), (0, 0, 0), (1, 1, 1))
  print(move(p, 1))
  print(collision_3(
    ((0, 0, 0), (0, 0, 0), (1, 1, 1)),
    ((6, 6, 6), (0, 0, 0), (0, 0, 0))
  ))
  '''


test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve_easy(input)
print(result)
result = solve(input)
print(result)
