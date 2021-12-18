#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys

num = 0
for line in sys.stdin:
    for i, c in enumerate(line):
        if c == '(': num += 1
        if c == ')': num -= 1
        print i, c, num
        if num == -1:
            print i+1
            break
    break
