#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import hashlib
  

def find_zeroes(key, zeroes = 5):
    prefix = '0' * zeroes
    i = 0
    while True:
        i += 1
        message = "%s%s" % (key, i)
        hash = hashlib.md5(message).hexdigest()
        # print message, hash
        if hash.startswith(prefix):
            return i


def test():
    assert find_zeroes('abcdef') == 609043


def a():
    return find_zeroes(sys.stdin.next())

def b():
    return find_zeroes(sys.stdin.next(), 6)

# test()
# print a()
print b()
