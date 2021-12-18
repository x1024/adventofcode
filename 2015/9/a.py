#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools


def solve(routes, aggregate = min):
    distances = {}
    cities = set()
    for route in routes:
        path, distance = map(lambda x: x.strip(), route.split('='))
        city_a, city_b = map(lambda x: x.strip(), path.split('to'))
        # print city_a, city_b, distance
        cities.add(city_a)
        cities.add(city_b)
        key = tuple(sorted((city_a, city_b)))
        distances[key] = int(distance)
    # print distances
    cities = list(cities)

    def cost(route):
        total = 0
        for i in xrange(len(route) - 1):
            city_a = route[i]
            city_b = route[i + 1]
            key = tuple(sorted((city_a, city_b)))
            total += distances[key]
        return total

    best_route = aggregate(cost(cities_route)
                           for cities_route in itertools.permutations(cities))
    return best_route


def easy(routes):
    return solve(routes, min)


def hard(routes):
    return solve(routes, max)


def test():
    routes = '''
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    '''
    routes = [line.strip() for line in routes.split("\n") if line.strip()]
    assert easy(routes) == 605
    assert hard(routes) == 982



test()
routes = list(sys.stdin)
print easy(routes)
print hard(routes)
