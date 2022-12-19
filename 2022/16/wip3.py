import IPython
import collections
import numpy
import pprint
import re
import queue


def score(minute, open):
  return 0

MAX = 9999
def shortest_paths(start, paths):
  data = []
  l = len(paths)
  for x in range(l):
    data.append([MAX] * l)
  for x in range(l):
    data[x][x] = 0
    for p in paths[x]:
      data[x][p] = 1
  for x in range(l):
    for y in range(l):
      for j in range(l):
        if data[x][j] + data[j][y] < data[x][y]:
            data[x][y] = data[x][j] + data[j][y]

  for row in data: print(row)
  return data


def solve(input):
  tunnels = [[] for i in input]
  flows = [0 for i in input]
  valves = [i[0] for i in input]
  valves = list(sorted(valves))
  for valve, flow, paths in input:
    valve = valves.index(valve)
    paths = [valves.index(p) for p in paths]
    tunnels[valve] = paths
    flows[valve] = flow

  spaths = shortest_paths(valves.index('AA'), tunnels)

  full_valves = list(sorted([valves.index(v) for v, flow, paths in input if flow > 0]))
  print(full_valves)
  
  q = queue.PriorityQueue()
  scores = {}

  def add(minute, p1, _open, negative_current_score):
    q.put((minute, p1, tuple(sorted(_open)), negative_current_score))

  add(0, valves.index('AA'), tuple([0 for i in full_valves]), -0)
  max_minutes = 30 - 4
  i = 0

  max_score = 0
  while not q.empty():
    pos = q.get()
    minute, current1, _open, negative_current_score = pos
    _open = tuple(sorted(_open))
    tmp = (minute, current1, _open)
    if minute > max_minutes: continue
    if tmp in scores: continue
    scores[tmp] = -1 * negative_current_score
    i += 1

    if i % 10000 == 0:
      max_score = max(scores.values())
      score = -1 * negative_current_score
      for key, value in scores.items():
        if value == max_score:
          print(key)
      print(minute, tmp, score, max_score)
    
    # open
    if not current1 in _open:
      flow1 = flows[current1]
      add1 = flow1 * (max(0, max_minutes - (minute + 1)))
      new_score = negative_current_score - add1
      add(minute + 1, current1, _open + (current1, ), new_score)

    # move
    for t1 in full_valves:
      time = spaths[current1][t1]
      add(minute + time, t1, _open, negative_current_score)

  result = max(scores.values())
  return result


def parse_line(input):
  input, tunnels = input.split(";")
  tunnels = tunnels.replace(",", "").split()[4:]
  words = input.split()
  valve = words[1]
  flow = int(words[4].split("=")[-1])
  return (valve, flow, tunnels)


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  print(result == 1707)
  return


test()
exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# IPython.embed()
