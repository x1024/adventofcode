import IPython
import collections
import numpy
import pprint
import re
import queue


def score(minute, open):
  return 0


def solve(input):
  tunnels = {}
  flows = {}
  for valve, flow, paths in input:
    tunnels[valve] = paths
    flows[valve] = flow

  q = queue.PriorityQueue()
  scores = {}
  start = (0, 'AA', tuple(), -0)
  q.put(start)
  max_minutes = 30
  i = 0

  while not q.empty():
    pos = q.get()
    minute, current, _open, negative_current_score = pos
    tmp = (minute, current, _open)
    if minute > max_minutes: continue
    if tmp in scores: continue
    scores[tmp] = -1 * negative_current_score
    i += 1
    if i % 10000 == 0:
      print(minute, tmp, -1 * negative_current_score, max(scores.values()))
    for t in tunnels[current]:
      flow = flows[t]
      if flow > 0 and not t in _open:
        new_score = negative_current_score - flow * (max(0, max_minutes - (minute + 2)))
        q.put((minute + 2, t, _open + (t, ), new_score))
      q.put((minute + 1, t, _open, negative_current_score))
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
  print(result == 1651)
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# IPython.embed()
