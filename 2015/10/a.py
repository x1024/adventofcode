#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import functools


def process(line):
    current = line[0]
    counter = 0
    total = []
    for i in line:
        if i == current:
            counter += 1
        else:
            total.append((counter, current))
            current = i
            counter = 1
    total.append((counter, current))
    # print total
    return ''.join(map(lambda i: ''.join(map(str, i)), total))


def test():
    assert process('1') == '11'
    assert process('11') == '21'
    assert process('21') == '1211'
    assert process('1211') == '111221'
    assert process('111221') == '312211'


def solve(line, repetitions):
    for i in xrange(repetitions):
        line = process(line)
    return len(line)


def easy(line):
    return solve(line, 40)


def hard(line):
    return solve(line, 50)


test()
line = sys.stdin.next().strip()
print easy(line)
print hard(line)
