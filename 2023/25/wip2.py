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
    for r in itertools.combinations(e, 3):
        # r = ( 'hfx/pzl', 'bvb/cmg', 'nvd/jqt' )
        # print(r)

        for k in r:
            a, b = k
            routes[a].remove(b)
            routes[b].remove(a)

        ls = set([tuple(sorted(bfs(node))) for node in routes])
        found = set()
        components = {}
        for node in routes:
            seen = bfs(node)
            for s in seen:
                if s in found: break
            else:
                components[node] = seen
            found.update(seen)

        if len(components) == 2:
            v = [len(c) for c in components.values()]
            print(r, v[0] * v[1])
            return v[0] * v[1]

        for k in r:
            a, b = k
            routes[a].add(b)
            routes[b].add(a)


data_test = open('input-sample.txt', 'r').read().strip()
result = main(data_test)
print("Test Result: {}".format(result))

# exit()

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
