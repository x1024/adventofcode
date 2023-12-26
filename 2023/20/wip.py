import collections
import numpy
import pprint
import re
import functools
import itertools
import time
import math


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def solve(graph, start, end):
    q = collections.deque()
    q.append((start, [start]))
    while q:
        node, path = q.popleft()
        for next in graph[node] - set(path):
            if next == end:
                yield path + [next]
            else:
                q.append((next, path + [next]))

data = [row.strip() for row in open('input.txt', 'r').read().strip().split('\n')]

d = {}
for row in data:
    source, sink = row.split(" -> ")
    sink = sink.split(", ")
    if source == 'broadcaster':
        type = 'broadcaster'
    else:
        type, source = source[0], source[1:]
    d[source] = (type, sink)

def initliaze_memory():
    mem = dict((row.split(" ->")[0].replace('&', '').replace('%', ''), {}) for row in data)
    for row in data:
        source, sink = row.split(" -> ")
        source = source.replace('&', '').replace('%', '')
        sink = sink.split(", ")
        for s in sink:
            v = d.get(s, None)
            if not v: continue
            mem[s].update({source: 0})
    return mem

def run(start='broadcaster', target=None):
    q = collections.deque()
    q.append((start, 'button', 0))

    pulses = {}
    while q:
        node, _from, pulse = q.popleft()
        pulses[pulse] = pulses.get(pulse, 0) + 1

        if node not in d: continue
        if node == target and pulse == 1: return -1, -1
        type, sinks = d[node]
        memory = mem[node]
        if type == '%':
            if pulse == 1: continue
            memory['state'] = pulse = not memory.get('state', 0)
        elif type == '&':
            memory[_from] = pulse
            pulse = sum(memory.values()) < len(memory)
        q += [(sink, node, pulse) for sink in sinks]

    return pulses

mem = initliaze_memory()
h, l = functools.reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), (tuple(run().values()) for _ in range(1000)), (0, 0))
print(h * l)

mem = initliaze_memory()
part2 = functools.reduce(lcm, [
    (2 + max(itertools.takewhile(lambda x: run(node, 'lx') != (-1, -1), itertools.count())))
    for node in d['broadcaster'][1]
])
print(part2)

