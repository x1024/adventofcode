#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import collections


def parse(line):
    return map((lambda row: list(''.join(sorted(f))
                            for f in row.split(' '))),
        line.split(" | "))


def easy(data):
    return sum(
            sum(len(cell) in [2, 3, 4, 7] for cell in row[1])
        for row in map(parse, data.split('\n')))


def hard(data):
    return sum(map(solve, map(parse, data.split('\n'))))


def solve(row):
    first, second = row
    total = map(set, (first + second) * 10)
    digits = collections.defaultdict(lambda: set())
    def common(digit, b):
        return len(digits[digit].intersection(b))
    while len(digits) < 10:
        for s in total:
            if s in digits.values(): continue
            if len(s) == 2: digits[1] = s
            elif len(s) == 3: digits[7] = s
            elif len(s) == 4: digits[4] = s
            elif len(s) == 7: digits[8] = s
            elif len(s) == 5:
                if common(1, s) == 2: digits[3] = s
                elif common(6, s) == 5: digits[5] = s
                elif 5 in digits and 3 in digits: digits[2] = s
            elif len(s) == 6:
                if common(1, s) == 1: digits[6] = s
                elif (common(7, s) == 3 and common(1, s) == 2 and common(4, s) == 4): digits[9] = s
                elif 6 in digits and 9 in digits: digits[0] = s

    cypher = dict([(''.join(sorted(val)), key) for (key,val) in digits.items()])
    return int(''.join(str(cypher[digit]) for digit in second))


def test():
    data = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''
    assert easy(data) == 26
    assert hard(data) == 61229
    data = '''acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'''
    assert hard(data) == 5353


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

