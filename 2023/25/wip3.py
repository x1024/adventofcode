import collections
import numpy
import pprint
import re
import functools
import itertools

# First networkx library is imported  
# along with matplotlib 
import networkx as nx 
import matplotlib.pyplot as plt 
   
  
# Defining a Class 
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
        nx.draw_networkx(G) 
        plt.show() 


def main(data):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    d = {}
    routes = {}
    e = set()
    def add(a, b):
        # print(a, b)
        r1 = routes.get(a, set())
        r1.add(b)
        routes[a] = r1

        r2 = routes.get(b, set())
        r2.add(a)
        routes[b] = r2

        qwe = tuple(sorted((a, b)))
        e.add(qwe)
        # G.addEdge(a, b) 

      
    # G = GraphVisualization() 
    for row in data:
        key, edges = row.split(":")
        edges = edges.split()
        for edge in edges:
            add(key, edge)
    # G.visualize()
    print(routes)

    def bfs(start):
        seen = {}
        q = [(start, 0)]
        while q:
            node, dist = q.pop(0)
            seen[node] = seen.get(node, 0) + 1
            if seen[node] > 1: continue
            for edge in routes[node]:
                q.append((edge, dist + 1))
        return seen

    print(len(e))
    i = 0
    node = list(routes.keys())[0]
    # for r in itertools.combinations(e, 2):


    # r = [ ('dgt', 'tnz') ('rks', 'khz') ('gqm', 'ddc') ]
    r = [ ('dgt', 'tnz'), ('rks', 'kzh'), ('gqm', 'ddc') ]
    # r = ( 'hfx/pzl', 'bvb/cmg', 'nvd/jqt' )
    print(r)
    i += 1
    if i % 1000 == 0:
        print(i)

    for k in r:
        a, b = k
        routes[a].remove(b)
        routes[b].remove(a)

    found = set()
    components = {}

    seen = bfs(node)
    print(node)
    print(seen.values())
    if 1 in seen.values():
        ll = len(bfs(node))
        if ll < len(routes):
            print(ll, len(routes) - ll, ll * (len(routes) - ll))
            return ll * (len(routes) - ll)

    for k in r:
        a, b = k
        routes[a].add(b)
        routes[b].add(a)


data_test = open('input-sample.txt', 'r').read().strip()
# result = main(data_test)
# print("Test Result: {}".format(result))

# exit()

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()

