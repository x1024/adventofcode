#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import functools

def parse_coordinates(coordinates):
    return map(int, coordinates.split(','))


gates = [
    'AND',
    'OR',
    'LSHIFT',
    'RSHIFT',
    'NOT',
    # 'NOOP'
]

def memoize(func):
    cache = {}
    def memo(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return memo


def parse_line(line):
    strip = lambda x: x.strip()
    input, output = map(strip, line.split('->'))

    for gate in gates:
        if gate in input:
            parameters = map(strip,
                [i for i in input.split(gate) if i])
            return parameters, gate, output
    return input, 'NOOP', output


def process(data, initial_signal = 'a', bits = 16):
    signals = {}
    LIMIT = 2**bits - 1 

    @memoize
    def process_signal(name):
        if name.isdigit():
            return int(name)

        operation, input = signals[name]
        if operation == 'NOOP':
            return process_signal(input)
        if operation == 'AND':
            return process_signal(input[0]) & process_signal(input[1])
        if operation == 'OR':
            return process_signal(input[0]) | process_signal(input[1])
        if operation == 'RSHIFT':
            return process_signal(input[0]) >> int(input[1])
        if operation == 'LSHIFT':
            return process_signal(input[0]) << int(input[1])
        if operation == 'NOT':
            return LIMIT ^ process_signal(input[0])
        raise NotImplementedError()

    for line in data:
        input, operation, output = parse_line(line)
        signals[output] = (operation, input)

    for key in signals.keys():
        process_signal(key)

    return process_signal


def solve(data, initial_signal = 'a', bits = 16):
    func = process(data, bits)
    return func(initial_signal)


def test():
    # assert parse_line('NOT lk -> ll') == ('turn on', [[887, 9], [959, 629]])
    '''
    print solve([
        '123 -> x',
        '456 -> y',
        'x AND y -> d',
        'x OR y -> e',
        'x LSHIFT 2 -> f',
        'y RSHIFT 2 -> g',
        'NOT x -> h',
        'NOT y -> i',
    ], 'h')
    '''


def simple():
    return solve(sys.stdin)


def hard():
    inputs = [line for line in sys.stdin]
    func = process(inputs)
    a_value = func('a')
    print a_value
    inputs.append("%s -> b" % a_value)
    func = process(inputs)
    return func('a')

# test()
# print simple()
print hard()
# print b()
