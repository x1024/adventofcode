import math
import collections
import numpy
import pprint
import re
import functools
import itertools



def main(data):
    defs, values = data.split("\n\n")
    defs = [row.strip() for row in defs.strip().split('\n')]
    values = [row.strip() for row in values.strip().split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    defs2 = {}
    for row in defs:
        if not row: continue
        name, rules = row.replace("}", "").split("{")
        rules = rules.split(",")
        d2 = []
        for rule in rules:
            if ":" in rule:
                key, val = rule.split(":")
            else:
                key = "True"
                val = rule
            d2.append((key, val))
        defs2[name] = d2

    result = 0
    for row in values:
        scope = list(piece.split("=") for piece in row[1:-1].split(","))
        scope = dict((key, int(val)) for key, val in scope)
        score = sum(scope.values())
        # print(scope)
        workflow = 'in'
        while workflow in defs2:
            rules = defs2[workflow]
            # print(workflow)
            for rule, target in rules:
                if eval(rule, scope):
                    workflow = target
                    break
        print(workflow)
        if workflow == 'A':
            result += score
    # parse into a grid
    # map = {}
    # for r, row in enumerate(data):
    #     for c, col in enumerate(row):
    #         coord = (c + r * 1j)
    #         map[coord] = col
    print(result)
    r2 = []
    keys = {
        'x': 0,
        'm': 1,
        'a': 2,
        's': 3,
        '>': 1,
        '<': -1,
    }

    d3 = {}
    for key, rules in defs2.items():
        print(key, rules)
        r2 = []
        for rule, target in rules:
            if rule == 'True':
                r2.append((-1, -1, -1, target))
                continue
            var = rule[0]
            sign = rule[1]
            value = int(rule[2:])
            r2.append((keys[var], sign, value, target))
        d3[key] = r2

    @functools.lru_cache(maxsize=None)
    def solve(mins, maxs, workflow):
        if workflow == 'R': return 0
        if workflow == 'A':
            result = math.prod(maxs[key] - mins[key] + 1 for key in range(4))
            print(mins, maxs, workflow, result)
            return result
        print(workflow, mins, maxs)
        pprint.pprint(d3[workflow])
        # input()
        res = 0
        maxs = list(maxs)
        mins = list(mins)
        for var, sign, value, target in d3[workflow]:
            if var == -1:
                res += solve(tuple(mins), tuple(maxs), target)
                continue
            if sign == '<':
                old = maxs[var]
                maxs[var] = min(maxs[var], value - 1)
                res += solve(tuple(mins), tuple(maxs), target)
                maxs[var] = old
                mins[var] = max(mins[var], value)
            else:
                old = mins[var]
                mins[var] = max(mins[var], value + 1)
                res += solve(tuple(mins), tuple(maxs), target)
                mins[var] = old
                maxs[var] = min(maxs[var], value)
        return res

    LIM = 4000
    mins = tuple(( 1,1,1,1 ))
    maxs = tuple(( LIM, LIM, LIM, LIM ))
    print(solve(mins, maxs, 'in'))

    return result


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
