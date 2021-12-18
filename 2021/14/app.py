#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import collections


def parse_input(data):
    data = data.split("\n")
    polymer = data[0]
    steps = []
    for row in data[2:]:
        a, b = row.split(' -> ')
        s1 = a[0] + b
        s2 = b + a[1]
        step = a, (s1, s2)
        steps.append(step)
    steps = dict(steps)

    poly = collections.defaultdict(lambda: 0)
    for i in range(len(polymer) - 1):
        step = polymer[i:i+2]
        poly[step] += 1

    return poly, steps


def do_step(polymer, steps):
    poly = collections.defaultdict(lambda: 0)
    for step, count in polymer.items():
        sa, sb = steps[step]
        poly[sa] += count
        poly[sb] += count
    return poly


def do_step(polymer, steps):
    poly = collections.defaultdict(lambda: 0)
    for step, count in polymer.items():
        sa, sb = steps[step]
        poly[sa] += count
        poly[sb] += count
    return poly


def solve(data, l=40):
    polymer, steps = parse_input(data)

    for _ in range(l):
        polymer = do_step(polymer, steps)

    counts = collections.defaultdict(lambda: 0)
    for (poly, count) in polymer.items():
        counts[poly[0]] += count
        counts[poly[1]] += count

    # Most characters get counted twice for each occurrence
    # but the first and last characters get counted one time less.
    # Using (X + 1) / 2 instead of X / 2 handles that edge case.
    counts = [(value + 1)/2 for value in counts.values()]

    return (max(counts) - min(counts)) 


def hard(data):
    return solve(data, 40)


def easy(data):
    return solve(data, 10)


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
    assert easy(data) == 1588
    assert hard(data) == 2188189693529


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

