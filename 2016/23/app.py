#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections
import queue

def parse_input(data):
    return [row.strip().split(" ") for row in data.split("\n") if row]


def solve(data, registers = None, i = 0):
    data = parse_input(data)
    if not registers: registers = { 'a': 0, 'b': 0, 'c': 0, 'd': 0 }

    l = len(data)
    toggles = {
        'inc': 'dec',
        'dec': 'inc',
        'tgl': 'inc',
        'jnz': 'cpy',
        'cpy': 'jnz'
    }

    steps = 0
    while i < l:
        row = data[i]
        instruction = row[0]
        steps += 1

        if instruction == 'mul':
            _a = row[1]
            if _a in registers: _a = registers[_a]
            _b = row[2]
            if _b in registers: _b = registers[_b]
            _to = row[3]
            value = _a * _b
            registers[_to] = value
            i += 1
        elif instruction == 'add':
            _a = row[1]
            if _a in registers: _a = registers[_a]
            _b = row[2]
            if _b in registers: _b = registers[_b]
            _to = row[3]
            value = _a + _b
            registers[_to] = value
            i += 1
        elif instruction == 'noop':
            i += 1
        elif instruction == 'cpy':
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
                value = row[2]
                if value in registers:
                    value = registers[value]
                i += int(value)
            else:
                i += 1
        elif instruction == 'tgl':
            offset = row[1]
            if offset in registers:
                offset = registers[offset]
            target = i + offset
            if target >= 0 and target < len(data):
                row = data[target]
                target_instruction = row[0]
                new_instruction = toggles[target_instruction]
                row[0] = new_instruction
            i += 1
        else:
            print 'bad instruction', instruction
            exit()

    return registers['a']


def easy(data):
    return solve(data, { 'a': 7, 'b': 0, 'c': 0, 'd': 0 })


def hard(data):
    return solve(data, { 'a': 12, 'b': 0, 'c': 0, 'd': 0 })


def test():
    data = '''
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a'''
    assert solve(data) == 42

    data = '''cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a'''
    assert solve(data) == 3


if __name__ == '__main__':
    test()
    # data = sys.stdin.read()
    data = open('in.txt', 'r').read()
    print easy(data)

    # We can only optimize lines that we know for sure will never get executed
    # so this can only be done manually, after research
    data = open('in_fixed.txt', 'r').read()
    print hard(data)