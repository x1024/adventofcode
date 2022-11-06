import collections
import time


def parse_line(input):
  return [(0 if c == '.' else 1) for c in input]


def print_grid(grid):
  for i in range(-6, 9):
    for j in range(-6, 9):
      print('#' if grid[(i, j)] else '.', end="")
    print()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = map(int, input)
  input = [parse_line(line) for line in input]
  data = collections.defaultdict(lambda: 0)
  for i in range(len(input)):
    for j in range(len(input[0])):
      data[(i, j)] = input[i][j]
  # print_grid(input)
  start_pos = len(input) // 2, len(input[0]) // 2
  # print(start_pos)
  return data, start_pos

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
offsets = {
  UP: (-1, 0),
  RIGHT: (0, 1),
  DOWN: (1, 0),
  LEFT: (0, -1),
}

def solve(grid, start_pos = (1, 1), dir = UP, steps = 5):
  p = start_pos
  total = 0
  # print(initial)
  while steps > 0:
    steps -= 1
    g = grid[p]
    if g:
      dir = (dir + 1) % 4
      # turn right
      grid[p] = False
    else:
      # turn left
      dir = (dir - 1 + 4) % 4
      total += 1
      grid[p] = True
    # total += (not g) and not initial[p]
    o = offsets[dir]
    p = (p[0] + o[0], p[1] + o[1])
    # print(p, dir)
    # print_grid(grid)
    # time.sleep(0.01)
    
  # print(total)
  return total


def test():
  code = '''
    ..#
    #..
    ...
  '''
  input, start_pos = parse_input(code)
  result = solve(input, start_pos, steps=70)
  print(result)
  assert result == 41
  input, start_pos = parse_input(code)
  result = solve(input, start_pos, steps=10000)
  print(result)
  assert result == 5587


test()
code = open('input.txt', 'r').read().strip()
input, start_pos = parse_input(code)
result = solve(input, start_pos, steps=10000)
print("Result: {}".format(result))
