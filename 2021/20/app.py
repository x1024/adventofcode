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
    return code, image


def iterate(code, image, border = 0):
    def b(l):
        result = 0
        for c in l:
            result = result * 2 + c
        return result

    image = [[border, border] + row + [border,border] for row in image]
    image = [
        [border] * len(image[0]),
        [border] * len(image[0]),
    ] + image + [
        [border] * len(image[0]),
        [border] * len(image[0]),
    ]
    new_image = []
    for row in image:
        new_image.append([0] * len(image[0]))

    for i in range(1, len(image) -1):
        for j in range(1, len(image[0]) -1):
            ca = image[i-1][j-1:j-1+3]
            cb = image[i][j-1:j-1+3]
            cc = image[i+1][j-1:j-1+3]
            c = ca + cb + cc
            index = b(c)
            # if i == 1 and j == 1: print c, index, code[index]
            new_image[i][j] = code[index]
    
    if border == 0:
        border = code[b([0,0,0, 0,0,0, 0,0,0])]
    else:
        border = code[b([1,1,1, 1,1,1, 1,1,1])]
    l0 = len(image)
    l1 = len(image[0])
    for i in range(l0):
        new_image[i][0] = border
        new_image[i][l1-1] = border
    for j in range(l1):
        new_image[0][j] = border
        new_image[l0-1][j] = border
    return new_image


def count(image):
    return sum(cell for row in image for cell in row)


def solve(data, iterations=2):
    code, image = parse_input(data)
    while iterations > 0:
        image = iterate(code, image, 0)
        iterations -= 1
        if iterations == 0: break
        image = iterate(code, image, code[0] == 1)
        iterations -= 1
    return count(image)


def easy(data):
    return solve(data, 2)


def hard(data):
    return solve(data, 50)


def test():
    data = open('in_test.txt').read()
    assert easy(data) == 35
    assert hard(data) == 3351


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)
    # answer_easy, answer_hard = solve(data)
    # print answer_easy
    # print answer_hard


if __name__ == '__main__':
    main()