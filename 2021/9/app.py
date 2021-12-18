#!/usr/bin/env python
#-*- coding: UTF-8 -*-

def parse(data):
    data = data.split('\n')
    return (
        [[9 for _ in range(len(data[0]) + 2)]] + 
        [[9] + map(int, row) + [9] for row in data] +
        [[9 for _ in range(len(data[0]) + 2)]]
    )


def easy(data):
    caves = parse(data)
    return sum(
        (1 + caves[i][j]) * (caves[i][j] < caves[i+1][j]
        and caves[i][j] < caves[i-1][j]
        and caves[i][j] < caves[i][j+1]
        and caves[i][j] < caves[i][j-1])
        for i in range(1, len(caves) - 1)
        for j in range(1, len(caves[0]) - 1))


def hard(data):
    caves = parse(data)
    def dfs(i, j):
        if caves[i][j] >= 9: return 0
        caves[i][j] = 9
        return (1 + dfs(i+1,j) + dfs(i-1,j) + dfs(i,j+1) + dfs(i,j-1))

    return reduce(lambda a, b: a * b, list(sorted(dfs(i, j)
        for i in range(1, len(caves) - 1)
        for j in range(1, len(caves[0]) - 1)))[-3:])


def test():
    data = '''2199943210
3987894921
9856789892
8767896789
9899965678'''
    assert easy(data) == 15
    assert hard(data) == 1134


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

