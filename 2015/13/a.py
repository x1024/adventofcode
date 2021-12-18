#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools


def solve(routes, add_yourself=False):
    distances = {}
    nodes = set()
    for route in routes:
        city_a, city_b, distance = route
        # path, distance = map(lambda x: x.strip(), route.split('='))
        # city_a, city_b = map(lambda x: x.strip(), path.split('to'))
        # print city_a, city_b, distance
        nodes.add(city_a)
        nodes.add(city_b)
        key = (city_a, city_b)
        distances[key] = int(distance)

    if add_yourself:
        name = 'you'
        for node in nodes:
            distances[(name, node)] = 0
            distances[(node, name)] = 0
        nodes.add(name)

    nodes = list(nodes)
    # print nodes

    def cost(route):
        total = 0
        for i in xrange(len(route)):
            city_a = route[i]
            city_b = route[(i + 1) % len(route)]
            key1 = (city_a, city_b)
            key2 = (city_b, city_a)
            # print city_a, city_b, distances[key1], distances[key2]
            total += distances[key1]
            total += distances[key2]
        return total

    best_route = max(cost(cities_route) for cities_route in itertools.permutations(nodes))
    return best_route


def easy(lines):
    lines = map(parse_line, lines)
    return solve(lines)


def hard(lines):
    lines = map(parse_line, lines)
    return solve(lines, add_yourself=True)

def parse_line(line):
    first, rest = line.split('would')
    value, second = rest.split('happiness units by sitting next to')
    first = first.strip().strip('.')
    direction, value = value.strip().split(' ')
    if direction == 'gain':
        direction = 1
    else:
        direction = -1
    value = int(value) * direction

    second = second.strip().strip('.')
    # print first, second
    return (first, second, value)


def test():
    assert parse_line('Alice would gain 54 happiness units by sitting next to Bob.') == ('Alice', 'Bob', 54)
    assert parse_line('Bob would gain 54 happiness units by sitting next to Alice.') == ('Bob', 'Alice', 54)
    assert parse_line('Alice would lose 54 happiness units by sitting next to Bob.') == ('Alice', 'Bob', -54)
    data = '''
    Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.
    '''
    data = [line.strip() for line in data.split("\n")]
    data = [line for line in data if line]
    # print res
    assert easy(data) == 330
    assert hard(data) == 286



test()
routes = list(sys.stdin)
print easy(routes)
print hard(routes)
