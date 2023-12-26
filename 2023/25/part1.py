import collections
import numpy
import pprint
import re
import functools
import itertools


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

    for row in data:
        key, edges = row.split(":")
        edges = edges.split()
        for edge in edges:
            add(key, edge)

    def bfs(start):
        seen = set()
        q = [(start, 0)]
        while q:
            node, dist = q.pop(0)
            if node in seen:
                continue
            seen.add(node)
            for edge in routes[node]:
                q.append((edge, dist + 1))
        return seen

    print(len(e))
    i = 0
    asd = [
        [ ('dgt', 'tnz'), ('rks', 'kzh'), ('gqm', 'ddc') ]
    ]
    for r in asd:
        # r = ( 'hfx/pzl', 'bvb/cmg', 'nvd/jqt' )
        # print(r)
        i += 1
        if i % 1000 == 0:
            print(i)

        for k in r:
            print(k)
            a, b = k
            routes[a].remove(b)
            routes[b].remove(a)

        found = set()
        components = {}
        for node in routes:
            seen = bfs(node)
            ll = len(bfs(node))
            if ll < len(routes):
                print(ll, len(routes) - ll, ll * (len(routes) - ll))
                return ll * (len(routes) - ll)
            break

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
