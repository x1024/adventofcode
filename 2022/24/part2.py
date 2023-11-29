import queue
import functools

directions = { '@': (0 + 0j), '^': (-1 + 0j), 'v': (+1 + 0j), '<': ( 0 - 1j), '>': ( 0 + 1j) }
data = open('input.txt', 'r').read().strip("\n").split('\n')
size = (len(data) - 2, len(data[0]) - 2)
templates = [(complex(i - 1, j - 1), directions[col])
  for i, row in enumerate(data) for j, col in enumerate(row) if col in directions]


@functools.cache
def blizzards(tick):
  return set(complex(int(pos.real % size[0]), int(pos.imag % size[1]))
    for pos in ((pos + dir * tick) for pos, dir in templates))


def bfs(start, end, tick):
  seen = set()
  q = queue.Queue()
  q.put((tick, start))
  while not q.empty():
    state = q.get()
    if state in seen: continue
    seen.add(state)
    tick, pos = state
    for dir in directions.values():
      new_pos = pos + dir
      if new_pos == end: return tick + 1
      elif new_pos == start or (0 <= new_pos.real < size[0] and 0 <= new_pos.imag < size[1] and new_pos not in blizzards(tick + 1)):
       q.put((tick + 1, new_pos))


start, end = complex(-1, 0), complex(size[0], size[1]-1)
print(tick := bfs(start, end, 0))
tick = bfs(end, start, tick)
print(tick := bfs(start, end, tick))