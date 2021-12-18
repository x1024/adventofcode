#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools

def solve(line, time_left):
    (name, speed, duration, rest) = line

    total_distance = 0
    while time_left >= 0:
        time_travelled = min(duration, time_left)
        total_distance += time_travelled * speed
        time_left -= time_travelled
        time_left -= rest
    return (total_distance, name)


def easy(lines, limit = 2503):
    lines = map(parse_line, lines)
    winner = max(map(lambda l: solve(l, limit), lines))
    return winner[0]


def hard(lines, limit = 2503):
    lines = map(parse_line, lines)
    points = {}
    for line in lines:
        name = line[0]
        points[name] = 0

    # print lines
    for time in range(1, limit + 1):
        results = map(lambda l: solve(l, time), lines)
        winning_distance = max(result[0] for result in results)
        winners = [result[1] for result in results if result[0] == winning_distance]
        for winner in winners:
            points[winner] += 1
            # print winner

    result = 0
    winner = None
    for key, value in points.items():
        if value > result:
            result = value
            winner = key
    # print points
    # print winner
    return result


def parse_line(line):
    words = line.split(' ')
    name = words[0]
    speed = int(words[3])
    duration = int(words[6])
    rest = int(words[13])

    return (name, speed, duration, rest)


def test():
    assert parse_line('Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.') == ('Vixen', 19, 7, 124)

    data = '''
    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
    '''
    data = [line.strip() for line in data.split("\n")]
    data = [line for line in data if line]
    assert easy(data, 1000) == 1120
    assert hard(data, 1000) == 689



test()
routes = [line.strip() for line in list(sys.stdin)]
print easy(routes)
print hard(routes)
