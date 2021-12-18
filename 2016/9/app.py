#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections


def solve(string, recursive=False):
    result = 0
    i = 0
    while i < len(string):
        if string[i] == '(':
            e = string.find(')', i)
            # print i, e, string[i:e+1]
            size, repetitions = map(int, string[i:e+1].strip('()').split('x'))
            if recursive:
                segment = string[e+1:e+1+size]
                result += solve(segment, recursive=recursive) * repetitions
            else:
                result += size * repetitions
            i = e + size + 1
        else:
            result += 1
            i += 1

    return result

def easy(string):
    return solve(string, recursive=False)


def hard(string):
    return solve(string, recursive=True)


def test():
    assert easy('ADVENT') == 6
    assert easy('A(1x5)BC') == 7
    assert easy('(3x3)XYZ') == 9
    assert easy('A(2x2)BCD(2x2)EFG') == 11
    assert easy('(6x1)(1x3)A') == 6
    assert easy('X(8x2)(3x3)ABCY') == 18

    assert hard('(3x3)XYZ') == len('XYZXYZXYZ')
    assert hard('X(8x2)(3x3)ABCY') == len('XABCABCABCABCABCABCY')
    assert hard('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
    assert hard('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445


if __name__ == '__main__':
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)
