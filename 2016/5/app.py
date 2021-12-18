#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import hashlib

# encoding GeeksforGeeks using md5 hash
# function


def easy(door_id, characters = 8):
    result = []
    index = 0
    while True:
        code = '%s%s' % (door_id, index)
        digest = hashlib.md5(code).hexdigest()
        if digest.startswith('00000'):
            # print index, digest
            result.append(digest[5])
            if len(result) == characters:
                return ''.join(result)
        index += 1


def hard(door_id, characters = 8):
    result = {}
    index = 0
    while True:
        code = '%s%s' % (door_id, index)
        digest = hashlib.md5(code).hexdigest()
        if digest.startswith('00000'):
            i = int(digest[5], 16)
            if i < characters and i not in result:
                value = digest[6]
                result[i] = value
                print i, value, result
                if len(result) == characters:
                    return ''.join(b for a, b in sorted(result.items()))
        index += 1


def test():
    assert easy('abc') == '18f47a30'
    assert hard('abc') == '05ace8e3'


if __name__ == '__main__':
    test()
    data = 'ugkcyxxp'
    print easy(data)
    print hard(data)

