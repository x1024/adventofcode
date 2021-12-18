#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import collections


def parse_input_easy(data):
    data = data.split("\n")
    polymer = data[0]
    steps = []
    for row in data[2:]:
        steps.append(row.split(' -> '))
    steps = dict(steps)
    return polymer, steps


def do_step_easy(polymer, steps):
    new_polymer = []
    for i in range(len(polymer) - 1):
        segment = polymer[i:i+2]
        addition = steps[segment]
        new_polymer.append(segment[0])
        new_polymer.append(addition)
        # print segment, addition
    new_polymer.append(polymer[-1])
    new_polymer = ''.join(new_polymer)

    return new_polymer


def easy(data, l=10):
    polymer, steps = parse_input_easy(data)
    for i in range(l):
        polymer = do_step_easy(polymer, steps)

    # print polymer
    counter = collections.Counter(polymer)
    items = [b for (a, b) in counter.items()]
    print counter.items(), max(items), min(items)
    return max(items) - min(items)



def test():
    data = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''
    assert easy(data, 10) == 1588

    # "NCNBCHB"
    # "NBCCNBBBCBHCB"
    # "NBBBCNCCNBBNBNBBCHBHHBCHB"
    # "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"


def main():
    test()
    data = open('in.txt').read()
    print easy(data)


if __name__ == '__main__':
    main()

