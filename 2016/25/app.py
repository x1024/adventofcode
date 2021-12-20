#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections
import queue

def parse_input(data):
    return [row.strip().split(" ") for row in data.split("\n") if row]


def solve(data, registers = None, i = 0, callback = None):
    data = parse_input(data)
    if not registers:
        registers = { 'a': 0, 'b': 0, 'c': 0, 'd': 0 }

    l = len(data)

    toggles = {
        'inc': 'dec',
        'dec': 'inc',
        'tgl': 'inc',
        'jnz': 'cpy',
        'cpy': 'jnz'
    }

    def panic():
        print "PANIC! Infinite loop detected"
        print "(Yes, really)"
        return False

    steps = 0
    while i < l:
        row = data[i]
        instruction = row[0]
        steps += 1
        if instruction == 'mul':
            _a = row[1]
            if _a in registers: _a = registers[_a]
            else: _a = int(_a)
            _b = row[2]
            if _b in registers: _b = registers[_b]
            else: _b = int(_b)
            _to = row[3]
            value = _a * _b
            registers[_to] = value
            i += 1
        elif instruction == 'div':
            _a = row[1]
            if _a in registers: _a = registers[_a]
            else: _a = int(_a)
            _b = row[2]
            if _b in registers: _b = registers[_b]
            else: _b = int(_b)
            _to = row[3]
            value = _a // _b
            registers[_to] = value
            i += 1
        elif instruction == 'mod':
            _a = row[1]
            if _a in registers: _a = registers[_a]
            else: _a = int(_a)
            _b = row[2]
            if _b in registers: _b = registers[_b]
            else: _b = int(_b)
            _to = row[3]
            value = _a % _b
            registers[_to] = value
            i += 1
        elif instruction == 'add':
            _a = row[1]
            if _a in registers: _a = registers[_a]
            else: _a = int(_a)
            _b = row[2]
            if _b in registers: _b = registers[_b]
            else: _b = int(_b)
            _to = row[3]
            value = _a + _b
            registers[_to] = value
            i += 1
        elif instruction == 'noop':
            i += 1
        elif instruction == 'cpy':
            _from = row[1]
            if _from in registers: _from = registers[_from]
            else: _from = int(_from)
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
            if _from in registers: _from = registers[_from]
            else: _from = int(_from)
            value = row[2]
            if value in registers: value = registers[value]
            else: value = int(value)
            if _from != 0 and value == 0: return panic()
            if _from != 0:
                i += value
            else:
                i += 1
        elif instruction == 'jmp':
            offset = row[1]
            if offset in registers: offset = registers[offset]
            else: offset = int(offset)
            if offset == 0: return panic()
            i += offset
        elif instruction == 'tgl':
            offset = row[1]
            if offset in registers: offset = registers[offset]
            else: offset = int(offset)
            target = i + offset
            if target >= 0 and target < len(data):
                row = data[target]
                target_instruction = row[0]
                new_instruction = toggles[target_instruction]
                row[0] = new_instruction
            i += 1
        elif instruction == 'out':
            value = row[1]
            if value in registers: value = registers[value]
            else: value = int(value)
            if callback:
                callback(value)
            else:
                print "out", value
            i += 1
        else:
            print 'bad instruction', instruction
            exit()

    return registers['a']


def easy(data):
    # Discovered by disassembling the code
    LIM = 2534

    # we need a number that:
    # * is at least 2534
    # * has the following bitwise representation:
    #   (least-significant bit first:)
    #   0101010101... (ending in 1)
    n_b = ''
    n_d = 0
    while n_d < LIM:
        n_b += '10'
        n_d = int(n_b, 2)
        print n_b, n_d

    # solve(data, { 'a': n_d - LIM, 'b': 0, 'c': 0, 'd': 0 })
    return n_d - LIM


def hard(data):
    pass


def test():
    pass


if __name__ == '__main__':
    test()
    # data = sys.stdin.read()
    data = open('in_fixed.txt', 'r').read()
    data = open('in.txt', 'r').read()
    print easy(data)
    # print hard(data)