import collections
import numpy
import pprint
import re
import functools
import itertools

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

    d = {}
    for row in data:
        source, sink = row.split(" -> ")
        sink = sink.split(", ")
        if source == 'broadcaster':
            type = 'broadcaster'
        else:
            type, source = source[0], source[1:]
        # print(type, source, sink)
        d[source] = (type, sink, {})
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
            v[2].update({source: 0})


    def run():
        q = collections.deque()
        q.append(('broadcaster', 'button', 0))

        high = 0
        low = 0
        while q:
            node, _from, pulse = q.popleft()
            if pulse == 1: high += 1
            else: low += 1

            print(_from, pulse, " -> ", node)
            n = d.get(node, None)
            if not n: continue
            type, sinks, memory = n
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
                print("INV", memory)
                to_send = 1
                if sum(memory.values()) == len(memory):
                    to_send = 0

                print(to_send)
                for sink in sinks:
                    q.append((sink, node, to_send))
        return high, low

    h, l = 0, 0
    for x in range(1000):
        high, low = run()
        h += high
        l += low
        print(x, high, low, h, l)
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
