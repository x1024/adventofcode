#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys


def possible(triangle):
    a, b, c = sorted(triangle)
    return a + b > c


def easy(data):
    return sum (possible(map(int, row.split())) for row in data.split('\n'))


def hard(data):
    numbers = [ [], [], [], ]
    for row in data.split('\n'):
        a, b, c = map(int, row.split())
        numbers[0].append(a)
        numbers[1].append(b)
        numbers[2].append(c)
    numbers = numbers[0] + numbers[1] + numbers[2]
    return sum(possible(numbers[i:i+3]) for i in range(0, len(numbers), 3))


def test():
    pass


if __name__ == '__main__':
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)

