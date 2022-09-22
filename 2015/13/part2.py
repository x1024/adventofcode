import itertools

def parse_line(line):
  # Alice would gain 2 happiness units by sitting next to Bob.
  words = line.strip('.').split()
  a = words[0]
  b = words[-1]
  gl = words[2]
  val = int(words[3])
  if gl == 'lose':
    val = - val
  return a, b, val

def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  lines = map(parse_line, input)
  people = set()
  dist = {}
  for line in lines:
    _f, _t, val = line
    people.add(_f)
    people.add(_t)
    dist[(_f, _t)] = val
    # dist[(_t, _f)] = val

  for p in people:
    dist[(p, 'You')] = 0
    dist[('You', p)] = 0

  people.add('You')
  # print lines
  # input = map(int, input)
  return people, dist

def solve(input):
  people, dist = input
  print people
  maxval = 0
  minval = 0
  for p in itertools.permutations(people):
    total = 0
    l = len(p)
    for i in range(l):
      _f = p[i]
      _t = p[(i+1) % l]
      key1 = (_f, _t)
      key2 = (_t, _f)
      # print key1, key2
      total += dist[key2] + dist[key1]
    maxval = max(maxval, total)
    minval = max(minval, total)
  return max(abs(maxval), abs(minval))

input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
