#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import queue


def iterate(line):
    a = line
    b = (''.join(list(reversed(line)))
        .replace('0', '2')
        .replace('1', '0')
        .replace('2', '1'))
    return "%s0%s" % (a, b)


def checksum(line):
    if len(line) % 2 == 1: return line

    result = []
    for i in range(0, len(line) - 1, 2):
        if line[i] == line[i+1]:
            result.append('1')
        else:
            result.append('0')
    return checksum(''.join(result))


def solve(data, length):
    while len(data) < length: data = iterate(data)
    return checksum(data[:length])


def easy(data):
    return solve(data, 272)


def hard(data):
    return solve(data, 35651584)


def test():
    assert iterate('1') == '100'
    assert iterate('0') == '001'
    assert iterate('11111') == '11111000000'
    assert iterate('111100001010') == '1111000010100101011110000'
    assert checksum('110010110100') == '100'
    assert solve('10000', 20) == '01100'


if __name__ == '__main__':
    test()
    data = '11101000110010100'
    print easy(data)
    print hard(data)