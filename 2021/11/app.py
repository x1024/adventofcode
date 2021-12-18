#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def solve(input, steps):
    input = input.split('\n')
    INF = -99999999

    n = len(input)
    m = len(input[0])
    cells = [(i, j) for i in range(1, n + 1) for j in range(1, m + 1)]

    data = [[INF for _ in range(m + 2)] for _ in range(n + 2)]
    for (i, j) in cells: data[i][j] = int(input[i-1][j-1])

    neighbours = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        (+1, -1), (+1, 0), (+1, 1),
    ]

    flashes = 0
    step = 0
    while True:
        if step == steps: break # we reached the easy-mode endpoint

        step += 1
        step_flashes = 0  # What are you doing, step-flash?

        # add light
        for (i, j) in cells: data[i][j] += 1

        # calculate flashes, potentially n * m times
        while True:
            found_flash = False
            for (i, j) in cells:
                if data[i][j] < 10:
                    continue

                # flash the cell, adding energy to neighbours
                data[i][j] = INF
                found_flash = True
                step_flashes += 1
                for (x, y) in neighbours:
                    data[i + x][j + y] += 1

            if not found_flash:
                # no more energy has been added to the system
                break

        # Set just-flashed cells to 0
        for (i, j) in cells: data[i][j] = max(0, data[i][j])

        # hard-mode result
        if steps < 0 and step_flashes == n * m: return step

        flashes += step_flashes

    # easy-mode result
    return flashes


def easy(data):
    return solve(data, 100)


def hard(data):
    return solve(data, -1)


def test():
    data = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''
    assert easy(data) == 1656
    assert hard(data) == 195


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

