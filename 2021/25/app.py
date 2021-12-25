#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys


def parse_input(data):
    return [row.strip() for row in data.strip("\n").split("\n") ]


def print_board(data):
    for row in data:
        print >>sys.stderr, ''.join(row)


def iterate(data):
    moved = 0
    n = len(data)
    m = len(data[0])
    new_data = []
    for i in range(n):
        new_data.append(['.'] * m)

    for i in range(n):
        for j in range(m):
            c = data[i][j]
            if c == '>':
                ni, nj = i, (j+1) % m
                if data[ni][nj] == '.':
                    new_data[ni][nj] = c
                    moved += 1
                else:
                    new_data[i][j] = c
            elif c == 'v':
                new_data[i][j] = c
    data = new_data

    new_data = [['.'] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            c = data[i][j]
            if c == 'v':
                ni, nj = (i+1) % n, j
                if data[ni][nj] == '.':
                    new_data[ni][nj] = c
                    moved += 1
                else:
                    new_data[i][j] = c
            elif c == '>':
                new_data[i][j] = c
                
    return new_data, moved


def solve(data):
    data = parse_input(data)
    print_board(data)
    print >>sys.stderr, '----'
    cycle = 0

    while True:
        cycle += 1
        data, moved = iterate(data)
        print >>sys.stderr, cycle, moved
        print_board(data)
        print >>sys.stderr, '-----'
        if moved == 0: return cycle


def easy(data):
    return solve(data)


def hard(data):
    return solve(data)


def test():
    data = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''
    assert easy(data) == 58


def main():
    test()
    data = open('in.txt', 'r').read()
    print easy(data)


if __name__ == '__main__':
    main()