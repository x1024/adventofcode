import pprint
import collections

def solve(edges):
  # pprint.pprint(sorted(edges))
  used = set()
  route = []
  pos = 0
  max_len = 0
  def walk(pos):
    global max_len
    found = False
    l = sum(a+b for (a,b) in route)
    for edge in edges:
      if edge in used: continue
      if edge[0] == pos:
        found = True
        route.append(edge)
        used.add(edge)
        l = max(l, walk(edge[1]))
        used.remove(edge)
        route.pop()
      elif edge[1] == pos:
        found = True
        route.append(edge)
        used.add(edge)
        l = max(l, walk(edge[0]))
        used.remove(edge)
        route.pop()
    return l

  return walk(0)


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
  assert result == 31


test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
