#!/usr/bin/env python
#-*- coding: UTF-8 -*-

MAX_FISH_COUNTER = 10
MOTHER_FISH_COUNTER = 6
BABY_FISH_COUNTER = 8

def iterate(fish):
    new_fish = dict([(i, 0) for i in range(MAX_FISH_COUNTER)])
    new_fish[MOTHER_FISH_COUNTER] += fish[0]
    new_fish[BABY_FISH_COUNTER] += fish[0]

    for i in range(1, MAX_FISH_COUNTER):
        new_fish[i - 1] += fish[i]
    return new_fish


def easy(data, iterations = 80):
    data = map(int, data.split(','))
    fish = dict([(i, 0) for i in range(MAX_FISH_COUNTER)])

    for i in data:
        fish[i] += 1

    for _ in range(iterations):
        fish = iterate(fish)
    return sum(fish.values())


def hard(data):
    return easy(data, 256)


def test():
    data = '''3,4,3,1,2'''
    assert easy(data, 18) == 26
    assert easy(data) == 5934
    assert hard(data) == 26984457539


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

