#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
  
'''
It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
'''


def is_nice(string):
    for i in xrange(len(string) - 2): 
        if string[i] == string[i + 2]:
            break
    else:
        return False

    found = False
    for i in xrange(len(string) - 2): 
        for j in xrange(i + 2, len(string) - 1):
            if string[i] == string[j] and string[i + 1] == string[j + 1]:
                found = True
                break
        if found: break
    if not found: return False

    return True


def test():
    assert is_nice('qjhvhtzxzqqjkmpb') == True
    assert is_nice('xxyxx') == True
    assert is_nice('uurcxstgmygtbstg') == False
    assert is_nice('ieodomkazucvgmuy') == False


def main():
    return sum(is_nice(row) for row in sys.stdin)

test()
print main()
# print b()
