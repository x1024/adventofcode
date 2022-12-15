import pprint
import collections
import queue
import numpy
import IPython

offset = [
(-1, 0),
(+1, 0),
(0, -1),
(0, +1),
]

def solve(input):
  data, start, end = input
  pprint.pprint(start)
  q = queue.Queue()
  q.put((start, 0))
  n = len(data)
  m = len(data[1])
  data[start[0]][start[1]] = 0
  data[end[0]][end[1]] = 25
  seen = {}
  seen[start] = 0
  while not q.empty():
    now, steps = q.get()
    h = data[now[0]][now[1]]
    print('---', now)
    for d in offset:
      new_pos = now[0] + d[0], now[1] + d[1]
      if new_pos[0] < 0 or new_pos[0] >= n: continue
      if new_pos[1] < 0 or new_pos[1] >= m: continue
      if new_pos in seen: continue
      new_h = data[new_pos[0]][new_pos[1]]
      # print(new_h, h, new_h > h + 1)
      if new_h > h + 1: continue
      # print(new_pos)
      seen[new_pos] = steps + 1
      q.put((new_pos, steps + 1))
  result = seen[end]
  print(result)
  return result


def parse_line(input):
  return [ord(c) - ord('a') for c in input]


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  for x, row in enumerate(input):
    for y, col in enumerate(row):
      if col == -14:
        start = (x, y)
        print(start)
      if col == -28:
        end = (x, y)
        print(end)
  return input, start, end


def test():
  input = '''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
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

import pyperclip
pyperclip.copy(str(result))

IPython.embed()
