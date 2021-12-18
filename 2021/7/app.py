#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def cost(data, pos):
    return sum(abs(value - pos) for value in data)


def cost_hard(data, pos):
    return sum(abs(value - pos) * (abs(value - pos) + 1) / 2 for value in data)


def solve(data, cost_function = cost):
    data = map(int, data.split(','))
    min_cost = min(cost_function(data, i) for i in range(min(data), max(data)))
    return min_cost

def easy(data):
    return solve(data, cost)

def hard(data):
    return easy(data, cost_hard)


def test():
    data = '''16,1,2,0,4,2,7,1,2,14'''
    assert easy(data) == 37
    assert hard(data) == 168


def main():
    test()
    data = open('in.txt').read()
    print data
    print easy(data)
    print data
    print hard(data)


if __name__ == '__main__':
    main()

