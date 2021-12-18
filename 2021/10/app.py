#!/usr/bin/env python
#-*- coding: UTF-8 -*-

def parse(line):
    open = ['[', '<', '{', '(']
    # close = [']', '>', '}', ')']
    pairs = {
    ']': '[',
    '>': '<',
    '}': '{',
    ')': '(',
    }
    score = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    stack = []
    for i, c in enumerate(line):
        # print i, c, stack
        if c in open:
            stack.append(c)
            continue
        if len(stack) == 0:
            # print "stack empty"
            return score[c], stack
        end = pairs[c]
        if end != stack[-1]:
            # print "expected %s found %s, %s, %s" % (stack[-1], end, c, i)
            return score[c], stack
        stack.pop()
    return 0, stack


def easy(data):
    result = 0
    for line in data.split('\n'):
        err, _ = parse(line)
        result += err
        # print line, err, result
    return result

def hard(data):
    scores = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4,
    }
    all_scores = []
    for line in data.split('\n'):
        err, stack = parse(line)
        # print line, err, stack
        if err: continue
        score = 0
        for c in stack[::-1]:
            score = score * 5 + scores[c]
        all_scores.append(score)
    all_scores = list(sorted(all_scores))
    return all_scores[int(len(all_scores) / 2)]


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

