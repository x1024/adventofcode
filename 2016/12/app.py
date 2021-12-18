#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections
import queue

def parse_input(data):
    return [row.strip().split(" ") for row in data.split("\n") if row]


def solve(data, registers = None):
    data = parse_input(data)
    if not registers:
        registers = { 'a': 0, 'b': 0, 'c': 0, 'd': 0 }
    i = 0
    l = len(data)
    while i < l:
        row = data[i]
        instruction = row[0]
        # print row, registers
        if instruction == 'cpy':
            _from = row[1]
            if _from in registers:
                _from = registers[_from]
            _from = int(_from)
            _to = row[2]
            registers[_to] = _from
            i += 1
        elif instruction == 'inc':
            register = row[1]
            registers[register] += 1
            i += 1
        elif instruction == 'dec':
            register = row[1]
            registers[register] -= 1
            i += 1
        elif instruction == 'jnz':
            _from = row[1]
            if _from in registers:
                _from = registers[_from]
            if _from != 0:
                value = int(row[2])
                i += value
            else:
                i += 1
        else:
            print 'bad instruction'
            exit()
    return registers['a']


def easy(data):
    return solve(data)


def hard(data):
    return solve(data, { 'a': 0, 'b': 0, 'c': 1, 'd': 0 })


def test():
    data = '''
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a'''
    assert easy(data) == 42


if __name__ == '__main__':
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)