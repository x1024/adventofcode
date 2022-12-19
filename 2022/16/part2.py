import itertools
import IPython
import collections
import numpy
import pprint
import re
import queue


import networkx as nx
import matplotlib.pyplot as plt


MAX = 9999
def shortest_paths(paths):
  data = []
  l = len(paths)
  for x in range(l):
    data.append([MAX] * l)
  for x in range(l):
    data[x][x] = 0
    for p in paths[x]:
      data[x][p] = 1
  for j in range(l):
    for x in range(l):
      for y in range(l):
        if data[x][j] + data[j][y] < data[x][y]:
            data[x][y] = data[x][j] + data[j][y]
  return data


def draw_graph_optimized(nodes, edges, max_length, node_names):
  plt.clf()
  G = nx.Graph()
  l = len(nodes)
  for x in range(l):
    for y in range(x + 1, l):
      a = nodes[x]
      b = nodes[y]
      edge = edges[a][b] 
      if edge < max_length:
        na = node_names[a]
        nb = node_names[b]
        G.add_edge(na, nb, weight=edge)
  pos = nx.spring_layout(G, seed=7)
  nx.draw_networkx_nodes(G, pos, node_size=400)
  edges = [(u, v) for (u, v, d) in G.edges(data=True)]
  nx.draw_networkx_edges(
      G, pos, edgelist=edges, width=1, alpha=0.5, edge_color="b"
  )
  nx.draw_networkx_labels(G, pos, font_size=6, font_family="sans-serif")
  edge_labels = nx.get_edge_attributes(G, "weight")
  nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=4)
  ax = plt.gca()
  ax.margins(0.08)
  plt.axis("off")
  plt.tight_layout()
  plt.show(block=False)
  plt.savefig("graph_optimized.png", format="PNG", dpi=600)


def solve(input):
  tunnels = [[] for i in input]
  flows = [0 for i in input]
  valves = [i[0] for i in input]
  valves = list(sorted(valves))
  # Convert strings to integers, for easier indexing
  for valve, flow, paths in input:
    valve = valves.index(valve)
    paths = [valves.index(p) for p in paths]
    tunnels[valve] = paths
    flows[valve] = flow

  spaths = shortest_paths(tunnels)

  # Only use the valves that actually have something in them
  full_valves = list(sorted([valves.index(v) for v, flow, paths in input if flow > 0]))
  max_minutes = 30 - 4

  # draw_graph(input)
  # draw_graph_optimized([0] + full_valves, spaths, max_minutes, valves)

  l = len(spaths[0])
  memo = {}
  def get_paths(c):
    # how to most quickly visit the nodes in C
    if c in memo:
      return memo[c]
    length = len(c)
    max_score = -1
    for path in itertools.permutations(c):
      minutes = 0
      score = 0
      old = 0
      for i in range(0, length):
        new = path[i]
        minutes += spaths[old][new] + 1
        if minutes > max_minutes: break
        score += flows[new] * (max_minutes - minutes)
        old = new
      else:
        if score > max_score: max_score = score

    j = 0
    lc = len(c)
    for i in range(0, l):
      if j < lc and i == c[j]:
        j += 1
        continue
      if minutes + spaths[old][i] + 1 < max_minutes:
        # We can do "this path + at least 1 more node"
        # Therefore this path cannot be optimal
        max_score = -1
        break
    memo[c] = max_score
    return max_score

  res = 0
  for length in range(2, len(full_valves)):
    valid = 0
    # Visit c nodes total
    # First guy visits a, second guy visits b
    # One guy always gets no more than half of the nodes, obviously
    # The other guy gets about the same as the previous
    # E.g. we have 14 nodes and one guy takes 7:
    # The other guy can't take 3 -
    # this would've already been covered in the case where we have "10" results
    end = (length + 1) // 2

    # This is literally just guesstimating
    # It's possible to have an example where
    # "One guy gets 1 node, the other gets 10 nodes"
    # is the optimal solution
    # Therefore, this *might* take hours to finish
    # I basically just "Tried groups of up to N items, then up to N+1 items, etc."
    # Turns out that in the test data 7 is "the sweet spot"
    end = min(len(full_valves) // 2, end)
    # I have proven this mathematically, honest.
    # Definitely not a guesstimate at all
    start = max(1, end - 1)

    for i in range(start, end + 1):
      # first guy gets "i" items, second guy gets length - i
      # a is not longer than b, so we don't end up counting repeats
      print(i, length - i)
      if i > length - i: continue
      for a in itertools.combinations(full_valves, i):
        sa = get_paths(a)
        if sa == -1: continue
        rest = tuple( j for j in full_valves if j not in a )
        if max(rest) < min(a):
            # No valid permutations exist where b >= a
          continue
        for b in itertools.combinations(rest, length - i):
          if b < a: continue
          sb = get_paths(b)
          if sb == -1: continue
          new_res = sa + sb
          valid += 1
          if new_res > res:
            res = new_res
            # print(length, a, b, res, valid)
    print(length, res, valid)
    if valid == 0 and False:
      # If it's not possible to fulfill the path (e.g. one guy has to visit 40 nodes in 30 minutes), short-circuit
      break

  return res


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

def draw_graph(input):
  plt.clf()
  G = nx.Graph()
  edges = []

  flows = dict((name, int(valve)) for name, valve, _ in input)
  print(flows)
  for name, valve, paths in input:
    for path in paths:
      na, nb = sorted((name, path))
      if flows[na]: na += "\n(%s)" % flows[na]
      if flows[nb]: nb += "\n(%s)" % flows[nb]
      edges.append((na, nb))
      G.add_edge(na, nb)

  pos = nx.spring_layout(G, seed=7)
  # nx.draw_networkx(G, pos)
  nx.draw_networkx_nodes(G, pos, node_size=300)
  # print(edges)
  # edges
  nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="b", alpha=0.5, width=2)
  nx.draw_networkx_labels(G, pos, font_size=6, font_family="sans-serif")
  edge_labels = nx.get_edge_attributes(G, "weight")
  nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=4)

  ax = plt.gca()
  ax.margins(0.08)
  plt.axis("off")
  plt.tight_layout()

  plt.show(block=False)
  plt.savefig("graph.png", format="PNG", dpi=600)







# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# IPython.embed()
