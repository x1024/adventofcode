#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
  
'''
It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
'''


def is_nice(string):
    vowels = 'aeiou '
    forbidden = [ 'ab', 'cd', 'pq', 'xy' ]

    for i in xrange(len(string) - 1): 
        if string[i] == string[i + 1]:
            break
    else:
        return False

    for f in forbidden:
        if f in string:
            return False

    if sum(string.count(vowel) for vowel in vowels) < 3:
        return False
            
    return True


def test():
    assert is_nice('ugknbfddgicrmopn') == True
    assert is_nice('aaa') == True
    assert is_nice('jchzalrnumimnmhp') == False
    assert is_nice('haegwjzuvuyypxyu') == False
    assert is_nice('dvszwmarrgswjxmb') == False


def main():
    return sum(is_nice(row) for row in sys.stdin)

test()
print main()
# print b()
