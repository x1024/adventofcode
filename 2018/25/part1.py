


def distance(p1, p2):
  return (
    abs(p1[0] - p2[0]) + 
    abs(p1[1] - p2[1]) + 
    abs(p1[2] - p2[2]) + 
    abs(p1[3] - p2[3])
  )


def solve(points):
  groups = {}
  def group(g):
    while g != groups[g]:
      groups[g] = groups[groups[g]]
      g = groups[g]
    return g

  for i in range(len(points)): groups[i] = i
  while True:
    changed = False
    for i in range(len(points)):
      p1 = points[i]
      for j in range(i + 1, len(points)):
        p2 = points[j]
        g1 = group(i)
        g2 = group(j)
        # print(p1, p2, g1, g2)
        if g1 != g2 and distance(p1, p2) <= 3:
          changed = True
          groups[g2] = g1
          # print(i, j, g1, g2, groups)
    if not changed: break

  # print(len(set(groups.keys())), len(set(groups.values())))
  return len(set(groups.values()))


def parse_line(input):
  return tuple(map(int, input.split(',')))


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0'''
  print(solve(parse_input(input)))

  input = '''1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2'''
  print(solve(parse_input(input)))

  input = '''1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2'''
  print(solve(parse_input(input)))


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
