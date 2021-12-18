#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections


def check(row):
    brackets = 0
    result = False
    for i in range(len(row) - 3):
        if row[i] == '[': brackets += 1
        if row[i] == ']': brackets -= 1
        if row[i] == row[i + 3] and row[i + 1] == row[i + 2] and row[i] != row[i + 1]:
            if brackets:
                return False
            result = True
    return result


def check2(row):
    brackets = 0
    aba = []
    bab = []
    for i in range(len(row) - 2):
        segment = row[i:i+3]
        if row[i] == '[': brackets += 1
        elif row[i] == ']': brackets -= 1
        elif row[i] != row[i + 1] and row[i] == row[i + 2]:
            if ']' in segment: continue
            if '[' in segment: continue
            if brackets:
                bab.append(row[i:i+2])
            else:
                aba.append(row[i:i+2][::-1])
    return len(set(bab).intersection(aba)) > 0


def easy(data):
    return sum(map(check, data.split('\n')))


def hard(data):
    return sum(map(check2, data.split('\n')))


def test():
    assert check('abba[mnop]qrst') == True
    assert check('abcd[bddb]xyyx') == False
    assert check('aaaa[qwer]tyui') == False
    assert check('ioxxoj[asdfgh]zxcvbn') == True

    assert check2('aba[bab]xyz') == True
    assert check2('aaa[kek]eke') == True
    assert check2('zazbz[bzb]cdb') == True
    assert check2('xyx[xyx]xyx') == False


if __name__ == '__main__':
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)
