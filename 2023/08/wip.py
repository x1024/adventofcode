import re
import functools
import math

path, nodes = open('input.txt', 'r').read().strip().split('\n\n')
nodes = [re.sub('[^\w ]', '', row).split() for row in nodes.split('\n')]
nodes = dict((row[0], tuple(row[1:])) for row in nodes)

def solve(start, end):
    def period(node, i = 0):
        while True:
            node = nodes[node][path[i % len(path)] == 'R']
            i += 1
            if node in end: return i

    return functools.reduce(math.lcm, map(period, start))

start = [n for n in nodes if n.endswith('A')]
end = [n for n in nodes if n.endswith('Z')]
print(solve(['AAA'], ['ZZZ']), solve(start, end))
