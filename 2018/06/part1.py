import pprint
import collections
import numpy


def solve(input, LIMIT = 1000):
  areas = collections.defaultdict(lambda: 0)
  def check(x, y):
      distances = []
      for p in input:
        dx = abs(x - p[0])
        dy = abs(y - p[1])
        distances.append((dx + dy, p))
      distances = list(sorted(distances))[:2]
      if distances[0][0] == distances[1][0]:
        return False
      return distances[0][1]
  for x in range(-LIMIT, LIMIT):
    print(x)
    for y in range(-LIMIT, LIMIT):
      areas[check(x, y)] += 1
      # print(x, y, distances[:2])
  if False in areas: del areas[False]
  # check infinite
  MAX = LIMIT * 100
  infinite = collections.defaultdict(lambda: 0)
  for i in range(-MAX, MAX):
    x, y = (-MAX, i)
    infinite[check(x, y)] += 1
    x, y = (MAX, i)
    infinite[check(x, y)] += 1
    x, y = (i, MAX)
    infinite[check(x, y)] += 1
    x, y = (i, -MAX)
    infinite[check(x, y)] += 1
  if False in infinite: del infinite[False]
  for key in infinite:
    del areas[key]
  # pprint.pprint(infinite.keys())
  # pprint.pprint(areas)
  return max(areas.values())


def parse_line(input):
  return tuple(int(i) for i in input.split(','))


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
1, 1    
1, 6    
8, 3    
3, 4    
5, 5    
8, 9    
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
