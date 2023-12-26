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
    return result


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
