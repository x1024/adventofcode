#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import queue


def parse_input(data):
    def c(ch):
        if ch == '#': return 1
        else: return 0
    data = data.strip('\n').split("\n")
    code = map(c, data[0])
    image = [map(c, row) for row in data[2:]]

    border = 0

    image = [[border] * 1 + row + [border] * 1 for row in image]
    image = [
        [border] * len(image[0]),
        [border] * len(image[0]),
    ] + image + [
        [border] * len(image[0]),
        [border] * len(image[0]),
    ]

    return code, image


def iterate(code, image):
    def b(l):
        result = 0
        for c in l:
            result = result * 2 + c
        return result

    def transform(i, j):
        ca = image[i-1][j-1:j-1+3]
        cb = image[i][j-1:j-1+3]
        cc = image[i+1][j-1:j-1+3]
        c = ca + cb + cc
        index = b(c)
        return code[index]

    l0 = len(image) + 2
    l1 = len(image[0]) + 2

    # add old border
    border = image[0][0]
    image = [[border] + row + [border] for row in image]
    image = [[border] * l1] + image + [[border] * l1]

    # transform the "inner" part of the image
    new_image = [
        [transform(i, j) for j in range(1, l1 -1)]
        for i in range(1, l0 - 1)
    ]

    # add new, transformed, border
    border = new_image[0][0]
    new_image = [[border] + row + [border] for row in new_image]
    new_image = [[border] * l1] + new_image + [[border] * l1]

    return new_image


def count(image):
    return sum(cell for row in image for cell in row)


def solve(data, iterations=2):
    code, image = parse_input(data)
    for _ in range(iterations): image = iterate(code, image)
    if image[0][0] == 1: return float('inf')
    return count(image)


def easy(data):
    return solve(data, 2)


def hard(data):
    return solve(data, 50)


def test():
    data = open('in_test.txt').read()
    assert easy(data) == 35
    assert hard(data) == 3351
    data = open('in.txt').read()
    assert solve(data, 1) == float('inf')
    assert solve(data, 2) == 5479
    assert solve(data, 3) == float('inf')


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()
