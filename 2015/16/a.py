#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools


expected = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}


def easy(data, limit = 100, calorie_limit = None):
    data = [line.strip() for line in data.split("\n")]
    data = [line for line in data if line]
    lines = map(parse_line, data)

    for (index, values) in lines:
        for key, value in values.items():
            if expected[key] != value:
                break
        else:
            # print index, values
            return index


def hard(data):
    data = [line.strip() for line in data.split("\n")]
    data = [line for line in data if line]
    lines = map(parse_line, data)

    greater_than = [ 'cats', 'trees' ]
    less_than = [ 'pomeranians', 'goldfish' ]

    for (index, values) in lines:
        for key, value in values.items():
            if key in greater_than:
                if value <= expected[key]:
                    break
            elif key in less_than:
                if value >= expected[key]:
                    break
            elif expected[key] != value:
                break
        else:
            return index


def parse_line(line):
    # Sue 1: goldfish: 9, cars: 0, samoyeds: 9
    words = line.split(' ')
    # print words
    index = int(words[1].strip(':'))
    result = {}
    for i in xrange(2, len(words), 2):
        name = words[i].strip(":")
        value = int(words[i + 1].strip(","))
        result[name] = value
    return index, result


def test():
    assert parse_line('Sue 1: goldfish: 9, cars: 0, samoyeds: 9') == (1, {
        'goldfish': 9,
        'cars': 0,
        'samoyeds': 9,
    })
    # assert easy(data) == 62842880
    # assert hard(data) == 57600000



test()
data = ''.join(list(sys.stdin))
print easy(data)
print hard(data)
