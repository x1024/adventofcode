#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def parse_input(data):
    data = data.split(' ')
    dx = map(int, data[2][2:-1].split('..'))
    dy = map(int, data[3][2:].split('..'))

    limit = int(max(map(abs, dx + dy)) * 1.1)
    ranges = [(x, y) for x in range(0, max(dx) + 1) for y in range(min(dy), max(map(abs, dy)) + 1)]
    return [(dx, dy), ranges]


def simulate(x, y, bbox):
    pos = (0, 0)
    min_y = min(bbox[1])
    while True:
        pos = (pos[0] + x, pos[1] + y)
        x -= int(x / (abs(x) or 1))
        y -= 1
        in_x = bbox[0][0] <= pos[0] <= bbox[0][1]
        in_y = bbox[1][0] <= pos[1] <= bbox[1][1]
        if in_x and in_y: return True
        if not in_x and x == 0: return False
        if pos[1] < min_y and y < 0: return False


def easy(data):
    bbox, ranges = parse_input(data)
    return max(y * (y + 1) / 2 for (x, y) in ranges if simulate(x, y, bbox))


def hard(data):
    bbox, ranges = parse_input(data)
    return sum(simulate(x, y, bbox) for (x, y) in ranges)


def test():
    data = '''target area: x=20..30, y=-10..-5'''
    assert easy(data) == 45
    assert hard(data) == 112


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()
