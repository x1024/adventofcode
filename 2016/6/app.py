#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections


def solve(data, combiner):
    data = data.split('\n')
    return ''.join(
        combiner((b, a) for (a, b) in collections.Counter(row[i] for row in data).items())[1]
            for i in range(len(data[0]))
    )



def easy(data):
    return solve(data, max)


def hard(data):
    return solve(data, min)


def test():
    data = '''eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar'''
    assert easy(data) == 'easter'
    assert hard(data) == 'advent'
    # assert hard(data) == '05ace8e3'


if __name__ == '__main__':
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)
