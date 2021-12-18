#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def parse(data):
    rows = [row.strip() for row in data.split('\n')]
    rows = [row.split(' ') for row in rows if row]
    rows = [(direction, int(length)) for (direction, length) in rows]
    return rows


def easy(data):
    rows = [row for row in data.split('\n')]
    rows = [row.strip() for row in rows]
    rows = [row for row in rows if row]

    l = len(rows[0])
    gamma = []
    epsilon = []
    for bit in range(0, l):
        count = 0
        for row in rows:
            count += row[bit] == '1'
        if count + count > len(rows):
            gamma.append('1')
            epsilon.append('0')
        else:
            gamma.append('0')
            epsilon.append('1')
    gamma = int(''.join(gamma[::1]), 2)
    epsilon = int(''.join(epsilon[::1]), 2)
    # print gamma, epsilon
    return gamma * epsilon


def hard(data):
    rows = [row for row in data.split('\n')]
    rows = [row.strip() for row in rows]
    rows = [row for row in rows if row]

    l = len(rows[0])
    gamma = []
    epsilon = []
    initial_rows = rows

    report1 = None
    report2 = None

    rows = initial_rows
    for bit in range(0, l):
        count = 0
        for row in rows:
            count += row[bit] == '1'
        if count + count >= len(rows):
            common = '1'
        else:
            common = '0'
        print common, rows
        rows = [row for row in rows if row[bit] == common]
        if len(rows) == 1:
            report1 = rows[0]
            break

    rows = initial_rows
    for bit in range(0, l):
        count = 0
        for row in rows:
            count += row[bit] == '1'
        if count + count >= len(rows):
            not_common = '0'
        else:
            not_common = '1'
        print not_common, rows
        rows = [row for row in rows if row[bit] == not_common]
        if len(rows) == 1:
            report2 = rows[0]
            break

        
    print report1
    print report2
    report1 = int(''.join(report1[::1]), 2)
    report2 = int(''.join(report2[::1]), 2)

    print report1, report2
    return report1 * report2




def test():
    data = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
    '''
    assert easy(data) == 198
    assert hard(data) == 230


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

