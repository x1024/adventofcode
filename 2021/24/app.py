#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections
import queue

def parse_input(data):
    return [row.strip().split(" ") for row in data.split("\n") if row]


def solve(data, input_stream = None, max_steps=99999999):
    i = 0
    input_stream_index = 0
    data = parse_input(data)
    registers = {}
    for x in range(26):
        c = chr(ord('a') + x)
        registers[c] = 0

    l = min(len(data), max_steps)
    keys = ['w','x','y','z']

    steps = 0
    while i < l:
        row = data[i][:3]
        instruction = row[0]
        steps += 1
        # if i >= 235:
        #     # print i, row, [(key, registers[key]) for key in keys]
        #     print i, row, ' '.join([str(registers[key]) for key in keys])
        if instruction == 'noop':
            # print "NOOP"
            i += 1
        elif instruction == 'mul':
            _a = row[1]
            if _a in registers: _a = registers[_a]
            else: _a = int(_a)
            _b = row[2]
            if _b in registers: _b = registers[_b]
            else: _b = int(_b)
            _to = row[1]
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
            _to = row[1]
            value = int(_a / _b) # _a // _b
            registers[_to] = value
            i += 1
        elif instruction == 'mod':
            _a = row[1]
            if _a in registers: _a = registers[_a]
            else: _a = int(_a)
            _b = row[2]
            if _b in registers: _b = registers[_b]
            else: _b = int(_b)
            _to = row[1]
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
            _to = row[1]
            value = _a + _b
            registers[_to] = value
            i += 1
        elif instruction == 'eql':
            _a = row[1]
            if _a in registers: _a = registers[_a]
            else: _a = int(_a)
            _b = row[2]
            if _b in registers: _b = registers[_b]
            else: _b = int(_b)
            value = 1 if _a == _b else 0
            _to = row[1]
            registers[_to] = value
            i += 1
        elif instruction == 'set':
            _b = row[2]
            if _b in registers: _b = registers[_b]
            else: _b = int(_b)
            _to = row[1]
            registers[_to] = _b
            i += 1
        elif instruction == 'inp':
            if input_stream:
                value = int(input_stream[input_stream_index])
                input_stream_index += 1
            else:
                value = int(raw_input('Enter number:'))
            # print 'input', value
            _to = row[1]
            registers[_to] = value
            # print i, ' '.join([str(registers[key]) for key in keys])
            i += 1
        else:
            print 'bad instruction', instruction
            exit()

    # print '----'
    # print ' '.join([str(registers[key]) for key in keys])
    # print '----'
    return registers


def easy(data):
    return solve(data)


def hard(data):
    return solve(data)


def test():
    data = '''inp x
mul x -1'''
    # print easy(data)
    data = '''inp z
inp x
mul z 3
eql z x'''
    # print easy(data)
    data = '''inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2'''
    print easy(data)
    # assert easy(data) == 5


def equivalent(file1, file2, input_stream, max_steps):
    data1 = open(file1, 'r').read()
    data2 = open(file2, 'r').read()
    result1 = solve(data1, input_stream, max_steps)
    print '---'
    # result2 = solve(data2, input_stream, max_steps)
    # print result1.values()
    # print result2.values()
    print result1['z']
    print program(input_stream)
    return True
    # return result1 == result2


def main():
    # test()
    # exit()
    data = open('in.txt', 'r').read()
    input_stream = '13579246899999'
    input_stream = '99999999999999'
    input_stream = 99999999999999
    start = 1111111
    end = 9999999

    for i in range(end, start - 1, -1):
        if i % 10000 == 0: print i
        s = str(i)
        if '0' in s: continue
        # v = solve(data, s, 18 * 5)['z']
        # print s, v
        val = program(s, 14)
        if val:
            val = ''.join(map(str, val))
            print s, val
            break

    for i in range(start, end + 1):
        if i % 10000 == 0: print i
        s = str(i)
        if '0' in s: continue
        # v = solve(data, s, 18 * 5)['z']
        # print s, v
        val = program(s, 14)
        if val:
            val = ''.join(map(str, val))
            print s, val
            break
    
    exit()

    i = 0
    while input_stream >= 10**13:
        s = str(input_stream)
        if '0' in s:
            index = s.index('0')
            # print "HAS ZERO", index, 14 - index, input_stream
            input_stream = input_stream - input_stream % (10 ** (14 - index-1))
            input_stream = input_stream - 1
            continue
            # print "HAD ZERO", index, input_stream
            # raw_input()
        # v2 = solve(data, s)['z']
        x, z = program(s)
        print input_stream, x, z
        if x == 0:
            input_stream -= 10 ** (14 - z)
            if x < 9:
                raw_input()
            # print "BAD CODE", input_stream
            # raw_input()
            continue

        if z == 0:
            print "VALID", input_stream
            exit()

        input_stream = input_stream - 1
        i += 1
        # if i == 10000: exit()
    max_steps = 600
    assert equivalent('in.txt', 'in-fixed.txt', input_stream, max_steps)
    # print solve(data, input_stream=input_stream)
    # print hard(data)

offsets_y = [15, 10, 2, 16, 12, 11, 5, 16, 6, 15, 3, 12, 10, 13 ]
offsets_x = [0, 0, 0, 0, -12, 0, -9, 0, 0, -14, -11, -2, -16, -14]
# offsets_x = [ 15, 15, 12, 13, -12, 10, -9, 14, 13, -14, -11, -2, -16, -14]
# offsets_z = [1, 1, 1, 1, 26, 1, 26, 1, 1, 26, 26, 26, 26, 26 ]
# special_x = [4, 6, 9, 10, 11, 12, 13]

ox = offsets_x
oy = offsets_y

def program(input_stream, limit=999):
    z = 0
    index = 0
    result = []

    for i in range(limit):
        x = (z % 26) + offsets_x[i]

        if offsets_x[i] >= 0:
            w = int(input_stream[index])
            index += 1
            z = z * 26 + w + offsets_y[i]
            digit = w
        else:
            # print z, z % 26, (z % 26) + offsets_x[i]
            x = (z % 26) + offsets_x[i]
            z = int(z / 26)
            digit = x
            # print result, digit
            # raw_input()
            if not (1 <= digit <= 9):
                return False

        result.append(digit)
  
        # print i, w, x, y, z, offsets_z[i]
    return result


# '12345678901234'
# 'XXXX5XXXXXXXXX'
# 'XXXX5X_XX_____'

# valid = []
if False:
    lim = 5
    for i in range(10**lim - 1, 10**(lim-1), -1):
        code = str(i) + '9' * (14 - lim)
        # code[4] = 5
        if '0' in code: continue
        # print code
        x, z = program(code, lim)
        if x == 0:
            print i, code, x, z
            valid.append(i)
            # raw_input()
        # print i, code, z

# code_so_far = valid[0]
# code = '99959'
# if True:
    # lim = 2
    # for i in range(10**lim - 1, 10**(lim-1), -1):
        # code = code_so_far + str(i) + '9' * (14 - lim)
        # # code[4] = 5
        # if '0' in code: continue
        # # print code
        # x, z = program(code, lim)
        # if x == 0:
            # print i, code, x, z
            # valid.append(i)
            # # raw_input()
        # # print i, code, z

# print valid[0]
# exit()

if __name__ == '__main__':
    main()