import functools
import queue


@functools.cache
def geo_index(pos):
  if pos == start: return 0
  if pos == target: return 0
  if pos[0] == 0: return pos[1] * 48271
  if pos[1] == 0: return pos[0] * 16807
  # print(pos, erosion_index((pos[0] - 1, pos[1])), erosion_index((pos[0], pos[1] - 1)))
  return erosion_index((pos[0] - 1, pos[1])) * erosion_index((pos[0], pos[1] - 1))


@functools.cache
def erosion_index(pos):
  return (geo_index(pos) + depth) % 20183


def tile(index):
  match index % 3:
    case 0: return '.'
    case 1: return '='
    case 2: return '|'


# test()
start = (0, 0)
lines = open('input.txt', 'r').read().strip().split("\n")
depth = int(lines[0].replace("depth: ", ""))
target = tuple(map(int, lines[1].replace("target: ", "").split(',')))

# depth = 510
# target = (10, 10)

# data = []
# for y in range(target[0] + 1):
#   row = ''.join(tile(erosion_index((x, y))) for x in range(target[1] + 1))
#   data.append(row)
# print('\n'.join(data))

offsets = (
  ( 0,  1),
  ( 0, -1),
  ( 1,  0),
  (-1,  0),
)

ROCK = 0
WET = 1
NARROW = 2

NEITHER = 0
GEAR = 1
TORCH = 2

tools = { 
  ROCK: (GEAR, TORCH),
  WET: (GEAR, NEITHER),
  NARROW: (TORCH, NEITHER),
}

'''
In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).
'''
import sys
sys.setrecursionlimit(10000)

def heuristic(pos):
  dx = abs(target[0] - pos[0])
  dy = abs(target[1] - pos[1])
  return dx + dy


seen = {}
q = queue.PriorityQueue()
q.put((0 + heuristic(start), 0, start, TORCH))
best_result = 999999999
while not q.empty():
  estimate, time, pos, tool = q.get()
  state = (pos, tool)
  if seen.get(state, best_result) <= time: continue
  if time + estimate >= best_result: continue
  seen[state] = time
  terrain = erosion_index(pos) % 3

  if pos == target:
    wait = (0 if tool == TORCH else 7)
    best_result = min(best_result, time + wait)
    print(best_result, len(seen))
    continue

  for t in tools[terrain]:
    q.put((time + 7 + heuristic(pos), time + 7, pos, t))

  for o in offsets:
    new_pos = (pos[0] + o[0], pos[1] + o[1])
    if new_pos[0] < 0 or new_pos[1] < 0: continue
    new_terrain = erosion_index(new_pos) % 3
    if tool in tools[new_terrain]:
      q.put((time + 1 + heuristic(new_pos), time + 1, new_pos, tool))

# print(start, target, depth)
print(sum(
  erosion_index((x, y)) % 3
    for x in range(target[0] + 1)
    for y in range(target[1] + 1)
))
print(best_result)

# for y in range(target[1] + 5):
#   for x in range(target[0] + 5):
#     pos = (x, y)
#     score = min(
#       seen.get((pos, GEAR), 9999999),
#       seen.get((pos, TORCH), 9999999),
#       seen.get((pos, NEITHER), 9999999),
#     )
#     print("%s%03d " % (tile(erosion_index(pos)), score), end="")
#   print()