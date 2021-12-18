#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys

def parse_coordinates(coordinates):
    return map(int, coordinates.split(','))


def parse_line(line):
    prefixes = [
        'toggle',
        'turn off',
        'turn on',
    ]

    for prefix in prefixes:
        if line.startswith(prefix):
            line = line[len(prefix):]
            break
    coordinates = map(parse_coordinates, line.split('through'))
    return prefix, coordinates


def simulate(data, LIMIT = 1000):
    lights = []
    for x in xrange(LIMIT):
        row = [False] * LIMIT
        lights.append(row)
    
    def evaluate(line):
        print line
        prefix, coordinates = line
        if prefix == 'toggle':
            def operation(x, y): lights[x][y] = not lights[x][y]
        if prefix == 'turn on':
            def operation(x, y): lights[x][y] = True
        if prefix == 'turn off':
            def operation(x, y): lights[x][y] = False
        start = coordinates[0]
        end = coordinates[1]

        for x in xrange(start[0], end[0] + 1):
            for y in xrange(start[1], end[1] + 1):
                operation(x, y)

    for line in map(parse_line, data):
        evaluate(line)
    print sum(sum(row) for row in lights)
    return sum(sum(row) for row in lights)


def test():
    assert parse_line('turn on 887,9 through 959,629') == ('turn on', [[887, 9], [959, 629]])
    assert simulate([ 'toggle 0,0 through 999,0' ]) == 1000


def main():
    return simulate(sys.stdin)

# test()
print main()
# print b()
