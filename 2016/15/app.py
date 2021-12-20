#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import queue


# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_2.7
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)

    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a / b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def parse_line(line):
    line = line.split(' ')
    return (int(line[3]), int(line[-1].strip('.')))

def parse_input(data):
    return map(parse_line, data.split('\n'))


def solve(data):
    data = parse_input(data)
    n = [row[0] for row in data]
    a = [(row[0] - (row[1] + (i + 1))) % row[0] for i, row in enumerate(data)]
    res = chinese_remainder(n, a)
    return res


def easy(data):
    return solve(data)


def hard(data):
    hard_data = '''Disc #%s has 11 positions; at time=0, it is at position 11.''' % len(data)
    return solve(data + "\n" + hard_data)


def test():
    data = '''Disc #1 has 5 positions; at time=0, it is at position 3.
Disc #2 has 2 positions; at time=0, it is at position 1.'''
    assert easy(data) == 1
    data = '''Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.'''
    assert easy(data) == 5


if __name__ == '__main__':
    test()
    data = open('in.txt', 'r').read()
    print easy(data)
    print hard(data)