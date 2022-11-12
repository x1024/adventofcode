import pprint
import collections

def solve(edges):
  # pprint.pprint(sorted(edges))
  used = set()
  best = {
    'length': 0,
    'strength': 0,
  }

  def walk(pos, bridge_length):
    strength = sum(a+b for (a,b) in used)
    if bridge_length > best['length'] or bridge_length == best['length'] and strength >= best['strength']:
      # print(best, bridge_length, strength, used)
      best['length'] = bridge_length
      best['strength'] = strength

    for edge in edges:
      if edge in used: continue
      if edge[0] == pos:
        used.add(edge)
        walk(edge[1], bridge_length + 1)
        used.remove(edge)
      elif edge[1] == pos:
        used.add(edge)
        walk(edge[0], bridge_length + 1)
        used.remove(edge)

  walk(0, 0)
  print(best)
  return best['strength']


def parse_line(input):
  return tuple(sorted(tuple(int(i) for i in input.split("/"))))


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
0/2
2/2 
2/3
3/4
3/5
0/1
10/1
9/10
  '''
  input = parse_input(input)
  result = solve(input)
  assert result == 19


test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
