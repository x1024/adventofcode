#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def easy(goal, START = 1, LIMIT = 1000):
    PRESENTS_PER_HOUSE = 10
    sieve = [0] * LIMIT

    for i in range(1, LIMIT):
        cur = i
        while cur < LIMIT:
            sieve[cur] += i * PRESENTS_PER_HOUSE
            cur += i

    for i in range(START, LIMIT):
        # print i, sieve[i], goal, goal - sieve[i]
        if sieve[i] >= goal:
            return i
    
    return easy(goal, LIMIT, LIMIT * 10)


def hard(goal, START = 1, LIMIT = 1000):
    COUNTER_LIMIT = 50
    PRESENTS_PER_HOUSE = 11
    sieve = [0] * LIMIT

    for i in range(1, LIMIT):
        cur = i
        counter = 0
        while cur < LIMIT:
            if counter >= COUNTER_LIMIT:
                break
            sieve[cur] += i * PRESENTS_PER_HOUSE
            cur += i
            counter += 1

    for i in range(START, LIMIT):
        # print i, sieve[i], goal, goal - sieve[i]
        if sieve[i] >= goal:
            return i
    
    return hard(goal, LIMIT, LIMIT * 10)



def test():
    assert easy(10) == 1
    assert easy(30) == 2
    assert easy(40) == 3
    assert easy(70) == 4
    assert easy(60) == 4
    assert easy(120) == 6


test()
goal = int(input())
print easy(goal)
print hard(goal)
