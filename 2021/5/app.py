#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def parse(line):
    a, b = line.split(" -> ")
    a = map(int, a.split(','))
    b = map(int, b.split(','))
    return (a, b)


def easy(data, LIMIT=20, diagonals=False):
    data = map(parse, data.split('\n'))
    array = []
    for i in range(LIMIT):
        array.append([0] * LIMIT)
    for row in data:
        a, b = row
        x1 = a[0]
        x2 = b[0]
        y1 = a[1]
        y2 = b[1]
        if x1 == x2 or y1 == y2:
            if x1 > x2:
                tmp = x1
                x1 = x2
                x2 = tmp

            if y1 > y2:
                tmp = y1
                y1 = y2
                y2 = tmp

            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    array[i][j] += 1
        elif diagonals:
            t = abs(y1 - y2)
            for i in range(0, t + 1):
                if x1 < x2:
                    x = x1 + i
                else:
                    x = x1 - i
                if y1 < y2:
                    y = y1 + i
                else:
                    y = y1 - i
                array[x][y] += 1
            
    result = 0
    for i in range(LIMIT):
        for j in range(LIMIT):
            result += array[i][j] >= 2

    return result


def hard(data, LIMIT=20):
    return easy(data, LIMIT, diagonals=True)


def test():
    data = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''
    assert easy(data, 20) == 5
    assert hard(data, 20) == 12


def main():
    test()
    data = open('in.txt').read()
    # print data
    print easy(data, 2000)
    print hard(data, 2000)


if __name__ == '__main__':
    main()

