#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import functools


def increment(password):
    i = len(password) - 1
    while True:
        if i < 0:
            break
        password[i] += 1
        if password[i] == 26:
            password[i] = 0
            i -= 1
        else:
            break
    return password


def encode_password(password):
    return map(lambda c: ord(c) - ord('a'), password)


def decode_password(password):
    return ''.join(map(lambda c: chr(c + ord('a')), password))


def valid_password(password):
    forbidden = map(lambda c: ord(c) - ord('a'), ('i', 'l', 'o'))
    for c in forbidden:
        if c in password:
            # print "forbidden"
            return False

    for i in xrange(len(password) - 2):
        if password[i] + 1 == password[i + 1] and password[i + 1] + 1 == password[i + 2]:
            break
    else:
        # print "no triples"
        return False

    found = 0
    i = 0
    while i < len(password) - 1:
        if password[i] == password[i + 1]:
            i += 1
            found += 1
        i += 1
    if found < 2:
        # print "no doubles"
        return False

    return True


def next_password(password):
    password = encode_password(password)
    while True:
        password = increment(password)
        # print decode_password(password), password
        if valid_password(password):
            return decode_password(password)
        # if decode_password(password).startswith('abcdff'): raw_input()


def solve(data, initial_signal = 'a', bits = 16):
    func = process(data, bits)
    return func(initial_signal)


def test():
    assert increment([0, 0, 0, 1]) == [0, 0, 0, 2]
    assert increment([0, 0, 0, 25]) == [0, 0, 1, 0]
    assert increment([0, 25, 25, 25]) == [1, 0, 0, 0]
    assert encode_password('aaaa') == [0, 0, 0, 0]
    assert encode_password('zzzz') == [25, 25, 25, 25]
    assert decode_password([25, 25, 25, 25]) == 'zzzz'
    assert decode_password([0, 0, 0, 0]) == 'aaaa'
    assert decode_password(encode_password('qwertyzxc')) == 'qwertyzxc'
    assert valid_password(encode_password('hijklmmn')) == False
    assert valid_password(encode_password('abbceffg')) == False
    assert valid_password(encode_password('abbcegjk')) == False
    assert valid_password(encode_password('abbcabcd')) == False
    assert valid_password(encode_password('bbceeabc')) == True
    assert next_password('abcdefgh') == 'abcdffaa'
    assert next_password('ghijklmn') == 'ghjaabcc'


def simple(password):
    return next_password(password)


def hard(password):
    return next_password(next_password(password))


# test()
password = sys.stdin.next().strip()
print simple(password)
print hard(password)
# print b()
