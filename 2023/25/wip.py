import collections
import numpy
import pprint
import re
import functools
import itertools
import random
import math
import matplotlib.pyplot as plt
import time


class FormatPrinter(pprint.PrettyPrinter):

    def __init__(self, formats):
        super(FormatPrinter, self).__init__()
        self.formats = formats

    def format(self, obj, ctx, maxlvl, lvl):
        if type(obj) in self.formats:
            return self.formats[type(obj)] % obj, 1, 0
        return pprint.PrettyPrinter.format(self, obj, ctx, maxlvl, lvl)



def main(data, answers = []):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    d = {}
    routes = {}
    def add(a, b):
        # print(a, b)
        r1 = routes.get(a, set())
        r1.add(b)
        routes[a] = r1

        r2 = routes.get(b, set())
        r2.add(a)
        routes[b] = r2

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

    # pprint.pprint(routes)
    LIM = 10000
    MULTIPLIER = 2.5
    pos = {}
    for k in routes:
        # pos[k] = 500, 500
        pos[k] = (random.randint(0, LIM), random.randint(0, LIM))

    attract = 1

    # help(plt.draw)
    # plt.ion()
    printer = FormatPrinter({numpy.float64: "%.2f", float: "%.2f", int: "%06X"})
    answers = [ tuple(sorted(i)) for i in answers ]

    def draw_edge(a, b):
        key = tuple(sorted((a, b)))
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        dx = x2 - x1
        dy = y2 - y1
        dist = numpy.sqrt(dx * dx + dy * dy)

        x = [x1, x2]
        y = [y1, y2]

        is_answer = key in answers
        color = 'blue'
        linewidth = 2
        if is_answer:
            color = 'red'
            linewidth = 1
            plt.text((x1 + x2) / 2, (y1 + y2) / 2, "%.02f" % dist)
        plt.plot(x, y, label="%s" % dist, c=color, linewidth=linewidth)

    def draw_chart():
        keys = pos.keys()
        x = [pos[k][0] for k in keys]
        y = [pos[k][1] for k in keys]
        plt.scatter(x, y, c ="blue")

        for k in sum(answers, tuple()):
            x, y = pos[k]
            plt.text(x, y, k, c="black")

        if len(routes) < 5000:
            # for key, dist in edges.items():
            for k, nodes in routes.items():
                for node in nodes:
                    draw_edge(k, node)
        else:
            for a, b in answers:
                draw_edge(a, b)

    while True:
        edges = []
        for k in routes:
            x, y = pos[k]
            for node in routes[k]:
                x2, y2 = pos[node]
                dx = x2 - x
                dy = y2 - y
                dist = numpy.sqrt(dx * dx + dy * dy)
                edges.append((dist, (k, node)))
                if dist > 0:
                    nx = dx / dist
                    ny = dy / dist
                    x += nx * attract * math.log(dist) * math.log(dist)
                    y += ny * attract * math.log(dist) * math.log(dist)
            pos[k] = (x, y)

        edges = list(sorted(edges))[-7:]
        # printer.pprint(edges)
        if edges[0][0] * MULTIPLIER < edges[-1][0]:
            edges_to_cut = list(set(tuple(sorted(edge[1])) for edge in edges[2::]))
            printer.pprint(edges_to_cut)
            break

        draw_chart()
        plt.draw()
        plt.pause(0.00001)
        plt.clf()

    # edges = list(reversed(sorted((val, key) for key, val in edges.items())))
    # printer.pprint([nodes for dist, nodes in edges[:6]])
    # r = ( 'hfx/pzl', 'bvb/cmg', 'nvd/jqt' )

    plt.clf()
    draw_chart()
    for k in edges_to_cut:
        # print(k)
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
            result = ll * (len(routes) - ll)
            title = "Edges: %s | Result: %s" % (', '.join('%s/%s' % edge for edge in edges_to_cut), result)
            print(title)
            plt.title(title)
            plt.draw()
            plt.show()
            return result
        break


data_test = open('input-sample.txt', 'r').read().strip()
answers = ( ('hfx', 'pzl'), ('bvb', 'cmg'), ('nvd', 'jqt') )
result = main(data_test, answers)
print("Test Result: {}".format(result))

# exit()

data = open('input.txt', 'r').read().strip()
answers = ( ('dgt', 'tnz'), ('rks', 'kzh'), ('gqm', 'ddc'))
result = main(data, answers)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
