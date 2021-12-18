#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys

'''
hlf r sets register r to half its current value, then continues with the next instruction.
tpl r sets register r to triple its current value, then continues with the next instruction.
inc r increments register r, adding 1 to it, then continues with the next instruction.
jmp offset is a jump
it continues with the instruction offset away relative to itself.
jie r, offset is like jmp, but only jumps if register r is even("jump if even").
jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).
'''


def easy(data, registers = None):
    data = [row.strip() for row in data.split('\n')]
    if registers is None:
        registers = { 'a': 0, 'b': 0 }
    index = 0
    while True:
        if index < 0 or index >= len(data):
            break
        row = data[index]
        row = row.split(' ')
        instruction = row[0]
        if instruction == 'hlf':
            register = row[1]
            registers[register] = registers[register] / 2
            index += 1
        elif instruction == 'tpl':
            register = row[1]
            registers[register] = registers[register] * 3
            index += 1
        elif instruction == 'inc':
            register = row[1]
            registers[register] = registers[register] + 1
            index += 1
        elif instruction == 'jmp':
            offset = int(row[1])
            index += offset
        elif instruction == 'jie':
            register = row[1].strip(',')
            offset = int(row[2])
            if registers[register] % 2 == 0:
                index += offset
            else:
                index += 1
        elif instruction == 'jio':
            register = row[1].strip(',')
            offset = int(row[2])
            if registers[register] == 1:
                index += offset
            else:
                index += 1
        else:
            raise NotImplementedError()

    print row, registers
    return registers


def hard(data):
    return easy(data, { 'a': 1, 'b': 0 })


def test():
    data = '''inc a
    jio a, +2
    tpl a
    inc a'''
    assert easy(data)['a'] == 2
    data.split('\n')


test()
data = sys.stdin.read()
# hp, attack, defense
print easy(data)['b']
print hard(data)['b']
# print hard(stats)
