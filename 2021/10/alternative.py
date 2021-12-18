#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def parse(line):
    while True:
        l = len(line)
        line = line.replace('()', '')
        line = line.replace('{}', '')
        line = line.replace('[]', '')
        line = line.replace('<>', '')
        if l == len(line): break
    indexes = [
        line.find(')'),
        line.find(']'),
        line.find('}'),
        line.find('>')
    ]
    indexes = [i for i in indexes if i > -1]
    return line, indexes


def easy(data):
    score = { ')': 3, ']': 57, '}': 1197, '>': 25137, }
    lines = [parse(line) for line in data.split('\n')]
    lines = [(line, indexes) for line, indexes in lines if indexes]
    return sum(score[line[min(indexes)]] for line, indexes in lines)


def hard(data):
    scores = { '(': 1, '[': 2, '{': 3, '<': 4, }
    lines = [parse(line) for line in data.split('\n')]
    lines = [(line, indexes) for line, indexes in lines if not indexes]
    all_scores = [
        reduce((lambda a, b: a * 5 + scores[b]), line[::-1], 0)
        for (line, _) in lines]
    return list(sorted(all_scores))[int(len(all_scores) / 2)]


def test():
    assert easy('{([(<{}[<>[]}>{[]{[(<()>') == 1197
    assert hard('<{([') == 294
    data = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''
    assert easy(data) == 26397
    assert hard(data) == 288957


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

