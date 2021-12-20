#!/usr/bin/env python
#-*- coding: UTF-8 -*-


trap_sequences = [ '^^.', '.^^', '^..', '..^' ]

def iterate(row):
    row = '.' + row + '.'
    return ''.join('^' if row[i-1:i+2] in trap_sequences else '.'
        for i in range(1, len(row) - 1))


def solve(data, iterations):
    result = 0
    for i in range(iterations):
        result += data.count('.')
        data = iterate(data)
    return result


def easy(data):
    return solve(data, 40)

def hard(data):
    return solve(data, 400000)


def test():
    rows = '''.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^'''.split('\n')
    for i in range(len(rows) - 1):
        assert iterate(rows[i]) == rows[i+1]

    assert solve(rows[0], 10) == 38


def main():
    test()
    data = open('in.txt').read().strip('\n')
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()