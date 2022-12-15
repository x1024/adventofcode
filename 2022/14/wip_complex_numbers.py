import sys

OFFSETS = [0+1j,-1+1j,1+1j]

def solve(data):
  sand = 0
  start = 500 + 0j

  first_dropped_sand = sys.maxsize
  max_y = max(pos.imag for pos in data)

  while True:
    pos = start
    while pos.imag < max_y + 1:
      try: pos = next(pos + offset for offset in OFFSETS if pos + offset not in data)
      except StopIteration: break
    else: first_dropped_sand = min(sand, first_dropped_sand)
    data.add(pos)
    sand += 1
    if pos == start: return first_dropped_sand, sand


def parse_line(line):
  return [tuple(map(int, cell.split(","))) for cell in line.split(" -> ")]


def parse_input(input):
  return set(complex(_x, _y)
    for row in map(parse_line, input.split('\n'))
      for (x, y), (nx, ny) in zip(row, row[1:])
        for _x in range(min(x, nx), max(x, nx) + 1)
          for _y in range(min(y, ny), max(y, ny) + 1))


def test():
  input = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print(f"Result: {result}")

import pyperclip
pyperclip.copy(str(result))

# IPython.embed()