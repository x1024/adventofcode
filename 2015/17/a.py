#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools


def easy(total, cups):
    l = len(cups)
    def solve(i, current = 0):
        # print i, current
        if i == l:
            if current == total:
                return 1
            else:
                return 0
        return solve(i+1, current) + solve(i+1, current + cups[i])

    # print solve(0)
    return solve(0)


def hard(total, cups):
    l = len(cups)
    solutions = {}
    def solve(i, current = 0, containers = 0):
        # print i, current, containers
        if i == l:
            if current == total:
                solutions[containers] = solutions.get(containers, 0) + 1
                return 1
            else:
                return 0
        return solve(i+1, current, containers) + solve(i+1, current + cups[i], containers + 1)

    solve(0)
    return solutions[min(solutions)]



def test():
    assert easy(25, [20, 15, 10, 5, 5]) == 4
    assert hard(25, [20, 15, 10, 5, 5]) == 3



test()
data = map(int, list(sys.stdin))
print easy(150, data)
print hard(150, data)
