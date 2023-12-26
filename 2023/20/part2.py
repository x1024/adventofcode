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

def main(data):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    mem = {}
    d = {}
    for row in data:
        source, sink = row.split(" -> ")
        sink = sink.split(", ")
        if source == 'broadcaster':
            type = 'broadcaster'
        else:
            type, source = source[0], source[1:]
        # print(type, source, sink)
        d[source] = (type, sink)
        mem[source] = {}

    for row in data:
        source, sink = row.split(" -> ")
        sink = sink.split(", ")
        if source == 'broadcaster':
            type = 'broadcaster'
        else:
            type, source = source[0], source[1:]
        for s in sink:
            v = d.get(s, None)
            if not v: continue
            mem[s].update({source: 0})


    presses = 0
    def run(start='broadcaster'):
        q = collections.deque()
        q.append((start, 'button', 0))

        high = 0
        low = 0
        while q:
            node, _from, pulse = q.popleft()
            if pulse == 1: high += 1
            else: low += 1

            # print(_from, pulse, " -> ", node)
            if node == 'lx' and pulse == 1:
                print('lx', pulse)
                return -1, -1
            if node == 'rx':
                if pulse == 0:
                    return -1, -1
            n = d.get(node, None)
            if not n: continue
            type, sinks = n
            if node not in mem:
                mem[node] = {}
            memory = mem[node]
            # print("\t", type, sinks, memory)
            if type == 'broadcaster':
                for sink in sinks:
                    q.append((sink, node, pulse))
            elif type == '%':
                if pulse == 1:
                    continue
                state = memory.get('state', 0)
                new_state = not state
                memory['state'] = new_state
                for sink in sinks:
                    q.append((sink, node, new_state))
            elif type == '&':
                memory[_from] = pulse
                # print("INV", memory)
                to_send = 1
                if sum(memory.values()) == len(memory):
                    to_send = 0

                # print(to_send)
                for sink in sinks:
                    q.append((sink, node, to_send))
        return high, low

    nodes = d['broadcaster'][1]
    print(nodes)
    res = []
    for node in nodes:
        presses = 0
        while True:
            presses += 1
            # if presses % 1000 == 0: print(node, presses)
            if run(node) == (-1, -1):
                res.append(presses)
                break
        print(node, presses)

    print(res)
    print(functools.reduce(lcm, res))
    exit()
    h, l = 0, 0
    while True:
        presses += 1
        high, low = run()
        h += high
        l += low
        # print(mem)
        # time.sleep(10)
        if presses % 1000 == 0:
            print(presses, high, low, h, l)
    print(h * l)
    return h * l


# data_test = open('input-sample.txt', 'r').read().strip()
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
