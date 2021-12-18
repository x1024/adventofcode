#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys

num = 0
for line in sys.stdin:
    for c in line:
        if c == '(': num += 1
        if c == ')': num -= 1
print num
