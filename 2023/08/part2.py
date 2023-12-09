import collections
import numpy
import pprint
import re
import functools
import itertools
import math

from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda acc, b: acc*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
 
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
 
 

def main(data):
    # pprint.pprint(data)
    instructions, data = data.split('\n\n')
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = list(map(int, data))
    print(instructions)

    result = 0

    r = {}
    for row in data:
        f, to = row.split(" = ")
        to = to.replace('(', '').replace(')', '').split(', ')
        r[f] = to

    print(r)
    start = []
    end = []
    for node in r:
        if node.endswith('A'):
            start.append(node)
        if node.endswith('Z'):
            end.append(node)

    def get_period(node, max=280 * 800):
        found = 0
        first, cycle = 0, 0
        cycles = []
        i = 0
        now = node
        while True:
            c = instructions[i % len(instructions)]
            dir = 0 if c == 'L' else 1
            now = r[now][dir]
            i += 1
            if i > max:
                return None
            if now in end:
                cycles.append(i)
                if len(cycles) >= 10:
                    return cycles

    cycles = {}
    for node in start:
        cycle = get_period(node)
        cycles[node] = cycle
        # print(node, cycle)

    result = 1
    for node in start:
        print(node, cycles[node])

    print(math.prod([cycles[node][0] for node in start]))
    # return (math.prod([cycles[node][0] for node in start]))
    return functools.reduce(lambda a, b: math.lcm(a, b), [cycles[node][0] for node in start])


    # print(cycles)
    exit()
    

    i = 0
    while True:
        c = instructions[i % len(instructions)]
        dir = 0 if c == 'L' else 1
        start = [r[s][dir] for s in start]
        done = [n for n in start if n in end]
        i += 1
        break
        if i % 1000000 == 0:
            print(i, start, end)
        if len(done) == len(start):
            return i

    return result


data_test = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''
# data_test = open('input-sample.txt', 'r').read().strip()
result = main(data_test)
print("Test Result: {}".format(result))

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
