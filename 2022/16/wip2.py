import IPython
import collections
import numpy
import pprint
import re
import queue


import networkx as nx
import matplotlib.pyplot as plt


class GraphVisualization:

    def __init__(self):

        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        pos = nx.spring_layout(G, seed=7)
        nx.draw_networkx(G, pos)
        plt.show(block=False)
        plt.savefig("Graph.png", format="PNG", dpi=600)


def score(minute, open):
  return 0


def solve(input):
  tunnels = {}
  flows = {}
  G = GraphVisualization()
  for valve, flow, paths in input:
    tunnels[valve] = paths
    flows[valve] = flow

  for valve, flow, paths in input:
    for path in paths:
      if flows[valve] > 0:
        a = "%s (%s)" % (valve, flows[valve])
      else:
        a = valve
      if flows[path] > 0:
        b = "%s (%s)" % (path, flows[path])
      else:
        b = path
      G.addEdge(a, b)
  G.visualize()

  return
  
  shortest_paths = {}

  q = queue.PriorityQueue()
  seen = set()
  scores = {}
  start = (0, 'AA', 'AA', tuple(), -0)
  q.put(start)
  max_minutes = 30 - 4
  i = 0

  while not q.empty():
    pos = q.get()
    minute, current1, current2, _open, negative_current_score = pos
    tmp = (minute, current1, current2, _open)
    if minute > max_minutes: continue
    if tmp in scores: continue
    scores[tmp] = -1 * negative_current_score
    i += 1
    if i % 10000 == 0:
      print(minute, tmp, -1 * negative_current_score, max(scores.values()))
    
    flow1 = flows[current1]
    add1 = flow1 * (max(0, max_minutes - (minute + 1)))
    flow2 = flows[current2]
    add2 = flow2 * (max(0, max_minutes - (minute + 1)))

    # open 1
    if flow1 > 0 and not current1 in _open:
      new_score = negative_current_score - add1
      q.put((minute + 1, current1, current2, _open + (current1, ), new_score))

    # open 2
    if flow2 > 0 and not current2 in _open:
      new_score = negative_current_score - add2
      q.put((minute + 1, current1, current2, _open + (current2, ), new_score))

    # open 1 and 2
    if flow1 > 0 and not current1 in _open and flow2 > 0 and not current2 in _open and not current1 == current2:
      new_score = negative_current_score - add1 - add2
      q.put((minute + 1, current1, current2, _open + (current1, current2, ), new_score))

    # 1 == 2, open 1
    if flow1 > 0 and not current1 in _open and current1 == current2:
      new_score = negative_current_score - add1
      q.put((minute + 1, current1, current2, _open + (current1, ), new_score))

    for t1 in tunnels[current1]:
      # move 1, open 2
      if flow2 > 0 and not current2 in _open:
        new_score = negative_current_score - add2
        q.put((minute + 1, t1, current2, _open + (current2, ), new_score))

      for t2 in tunnels[current2]:
        # open 1, move 2
        if flow1 > 0 and not current1 in _open:
          new_score = negative_current_score - add1
          q.put((minute + 1, current1, t2, _open + (current1, ), new_score))

        # move both
        q.put((minute + 1, t1, t2, _open, negative_current_score))

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


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

# import pyperclip
# pyperclip.copy(str(result))

# IPython.embed()
