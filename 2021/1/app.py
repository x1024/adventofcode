#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def easy(data):
    if len(data) == 0:
        return 0

    result = 0
    for i in xrange(1, len(data)):
        if data[i] > data[i-1]:
            result += 1
    return result


def hard(data):
    if len(data) < 3:
        return 0
    new_data = [sum(data[i:i+3]) for i in xrange(0, len(data) - 2)]
    return easy(new_data)


def test():
    data = [ 199, 200, 208, 210, 200, 207, 240, 269, 260, 263, ]
    assert easy(data) == 7
    assert hard(data) == 5


def main():
    test()
    data = open('in.txt').read().split('\n')
    data = [row.strip() for row in data]
    data = [int(row) for row in data if row]
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

