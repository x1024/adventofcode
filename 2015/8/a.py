#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys

def parse_line(line):
    a = eval(line)
    return len(line) - len(a)

def encode_line(line):
    a = '"' + line.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return len(a) - len(line)

def solve(data, initial_signal = 'a', bits = 16):
    func = process(data, bits)
    return func(initial_signal)


def test():
    assert parse_line('"aaa"') == 2
    lines = [ '""', '"abc"', '"aaa\\"aaa"', '"\\x27"', ]
    assert easy(lines) == 12
    assert hard(lines) == 19


def easy(lines):
    return sum(map(parse_line, lines))


def hard(lines):
    return sum(map(encode_line, lines))


test()
lines = [line.strip('\n') for line in sys.stdin]
print easy(lines)
print hard(lines)
# print b()
