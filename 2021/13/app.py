#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def parse_input(data):
    dots, folds = data.split('\n\n')
    dots = [map(int, row.split(',')) for row in dots.split('\n')]
    folds = [row.split('=')[0][-1] for row in folds.split('\n')]

    paper_x = max(a for (a, _) in dots) + 1
    paper_y = max(b for (_, b) in dots) + 1
    if paper_y % 2 == 0: paper_y += 1
    if paper_x % 2 == 0: paper_x += 1
    paper = [['.'] * paper_x for _ in range(paper_y)]
    for (a, b) in dots:
        paper[b][a] = '#'

    return paper, folds


def combine(paper1, paper2):
    y = len(paper1)
    x = len(paper1[0])
    result = [['.'] * x for _ in range(y)]
    for i in range(y):
        for j in range(x):
            if paper1[i][j] == '#' or paper2[i][j] == '#':
                result[i][j] = '#'
    return result


def fold_paper(paper, direction):
    if direction == 'y':
        distance = len(paper) / 2
        fold1 = paper[:distance]
        fold2 = paper[-distance:][::-1]
    else:
        distance = len(paper[0]) / 2
        fold1 = []
        fold2 = []
        for row in paper:
            fold1.append(row[:distance])
            fold2.append(row[-distance:][::-1])
    return combine(fold1, fold2)

 
def hard(data):
    paper, folds = parse_input(data)
    paper = reduce(fold_paper, folds, paper)
    return '\n'.join(
        ''.join(row).replace('#', '█').replace('.', ' ')
        for row in paper
    )


def easy(data):
    paper, folds = parse_input(data)
    paper = fold_paper(paper, folds[0])
    return sum(1 for row in paper for c in row if c == '#')



def test():
    data = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''
    assert easy(data) == 17
    print hard(data)


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

