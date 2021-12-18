#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections


def parse_line(line):
    source, checksum = line.split('[')
    checksum = checksum[:-1]
    code = source.split('-')
    sector_id = int(code[-1])
    source = '-'.join(code[:-1])
    code = ''.join(code[:-1])
    counts = sorted((-b, a) for (a, b) in collections.Counter(code).items())
    counts = ''.join(b for (a, b) in counts[:5])
    return counts == checksum, source, sector_id


def shift(letter):
    if letter < 'a' or letter > 'z': return letter
    return chr((ord(letter) - ord('a') + 1) % 26 + ord('a'))


def real_name(line):
    _, cypher, offset = parse_line(line)
    cypher = reduce(lambda cypher, _: map(shift, cypher), range(offset % 26), cypher)
    return (''.join(cypher).replace('-', ' '), offset)


def easy(data):
    def realness_score(line):
        isReal, _, sector_id = parse_line(line)
        return isReal * sector_id
    return sum(realness_score(line) for line in data.split('\n'))


def get_names(data):
    return [real_name(line) for line in data.split('\n')]


def hard(data):
    return dict(get_names(data))['northpole object storage']


def test():
    assert easy('aaaaa-bbb-z-y-x-123[abxyz]') == 123
    assert easy('a-b-c-d-e-f-g-h-987[abcde]') == 987
    assert easy('not-a-real-room-404[oarel]') == 404
    assert easy('totally-real-room-200[decoy]') == 0
    assert get_names('qzmt-zixmtkozy-ivhz-343[zimth]') == [('very encrypted name', 343)]


if __name__ == '__main__':
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)

