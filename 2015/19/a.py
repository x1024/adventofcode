#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import re
import queue


def parse_line(line):
    return line.strip("\n").split(' => ')


def easy(input, data):
    data = map(parse_line, data)
    result = set()
    for line in data:
        start, finish = line
        for m in re.finditer(start, input):
            index = m.start()
            new_input = input[:index] + finish + input[index + len(start):]
            # print index, input, start, finish, new_input
            result.add(new_input)

    return len(result)


def hard(start, data, goal = 'e'):
    data = map(parse_line, data)
    data = list(sorted([(b, a) for (a, b) in data]))

    q = queue.LifoQueue()
    q.put((0, start))
    seen = set()
    max_level = 0

    while not q.empty():
        level, input = q.get()

        if input == goal:
            return level

        for line in data:
            start, finish = line
            for m in re.finditer(start, input):
                index = m.start()
                new_input = input[:index] + finish + input[index + len(start):]
                if new_input in seen:
                    continue
                seen.add(new_input)
                q.put((level + 1, new_input))


def test():
    data = '''H => HO
H => OH
O => HH'''.split('\n')
    assert easy('HOH', data) == 4

    data = '''e => H
e => O
H => HO
H => OH
O => HH'''.split('\n')
    assert hard('HOH', data) == 3


test()
data = list(sys.stdin)
pairs = data[:-2]
input = data[-1]
print easy(input, pairs)
print hard(input, pairs)
