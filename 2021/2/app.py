#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def parse(data):
    rows = [row.strip() for row in data.split('\n')]
    rows = [row.split(' ') for row in rows if row]
    rows = [(direction, int(length)) for (direction, length) in rows]
    return rows


def easy(data):
    rows = parse(data)
    pos = [0, 0]

    for (direction, length) in rows:
        if direction == 'forward':
            pos[0] += length
        if direction == 'down':
            pos[1] += length
        if direction == 'up':
            pos[1] -= length

    result = pos[0] * pos[1]
    return result


def hard(data):
    rows = parse(data)
    pos = [0, 0, 0]

    for (direction, length) in rows:
        if direction == 'forward':
            pos[0] += length
            pos[1] += pos[2] * length
        if direction == 'down':
            pos[2] += length
        if direction == 'up':
            pos[2] -= length
        # print pos

    result = pos[0] * pos[1]
    return result





def test():
    data = '''
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2
    '''
    assert easy(data) == 150
    assert hard(data) == 900


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

