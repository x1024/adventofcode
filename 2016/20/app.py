#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def parse_input(data):
    return list(sorted(map(int, row.split('-')) for row in data.split("\n")))


def easy(data):
    data = parse_input(data)
    current = 0
    for (start, end) in data:
        if current < start: break
        current = max(current, end + 1)
    return current


def hard(data, limit=4294967295):
    data = parse_input(data)
    total = 0
    current = 0
    for (start, end) in data:
        total += max(0, start - current)
        current = max(current, end + 1)
    total += max(0, limit - current)
    return total


def test():
    data = '''5-8
0-2
4-7'''
    assert easy(data) == 3
    assert hard(data, 10) == 2


def main():
    import sys
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()