#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections


def solve(data, n=6, m=50):
    screen = [ ['.'] * m for i in range(n)]
    for row in data.split('\n'):
        if not row: continue
        row = row.split(' ')
        command = row[0]
        # print n, m, len(screen), len(screen[0]), row
        if command == 'rect':
            args = map(int, row[1].split('x'))
            for i in range(args[1]):
                for j in range(args[0]):
                    screen[i][j] = '#'
        if command == 'rotate':
            direction = row[1]
            index = int(row[2].split('=')[1])
            amount = int(row[4])
            if direction == 'row':
                screen[index] = screen[index][-amount:] + screen[index][:m - amount]
            else:
                array = [screen[i][index] for i in range(len(screen))]
                for i in range(len(array)):
                    screen[i][index] = array[(i - amount + len(array)) % len(array)]

    return screen


def easy(data, n=6, m=50):
    result = solve(data, n, m)
    return collections.Counter(sum(result, []))['#']


def hard(data, n=6, m=50):
    result = solve(data, n, m)
    return '\n'.join(''.join(''.join(row).replace('#', '█').replace('.', ' ')) for row in result)


def test():
    commands = [
        'rect 3x2',
        'rotate column x=1 by 1',
        'rotate row y=0 by 4',
        'rotate column x=1 by 1',
    ]

    results = [
        '''
        ###....
        ###....
        .......
        ''',

        '''
        #.#....
        ###....
        .#.....
        ''',

        '''
        ....#.#
        ###....
        .#.....
        ''',

        '''
        .#..#.#
        #.#....
        .#.....
        '''
    ]

    lights = [
        6, 6, 6, 6
    ]

    for i in range(len(commands)):
        input_commands = commands[:i + 1]
        expected = lights[i]
        actual = easy('\n'.join(input_commands), 3, 7)
        assert actual == expected

    for i in range(len(commands)):
        input_commands = commands[:i + 1]
        expected = ('\n'.join(row.strip()
            for row in results[i].strip('\n').split('\n'))
            .strip('\n').replace('#', '█').replace('.', ' '))
        actual = hard('\n'.join(input_commands), 3, 7)
        assert actual == expected


if __name__ == '__main__':
    test()
    data = open('in.txt', 'r').read()
    # data = sys.stdin.read()
    print easy(data)
    print hard(data)
