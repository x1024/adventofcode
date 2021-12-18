#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import json
import sys


def parse(obj):
    if type(obj) == dict: return sum(map(parse, obj.values()))
    if type(obj) == list: return sum(map(parse, obj))
    if type(obj) == str: return 0
    if type(obj) == unicode: return 0
    if type(obj) == str: return 0
    if type(obj) == int: return obj
    raise NotImplementedError(type(obj))


def parse_hard(obj):
    if type(obj) == dict:
        if 'red' in obj.keys() or 'red' in obj.values():
            return 0
        return sum(map(parse_hard, obj.values()))
    if type(obj) == list: return sum(map(parse_hard, obj))
    if type(obj) == str: return 0
    if type(obj) == unicode: return 0
    if type(obj) == str: return 0
    if type(obj) == int: return obj
    raise NotImplementedError(type(obj))



def test():
    assert parse([1,2,3]) == 6
    assert parse({"a":2,"b":4}) == 6
    assert parse([[[3]]]) == 3
    assert parse({"a":{"b":4},"c":-1}) == 3
    assert parse({"a":[-1,1]}) == 0
    assert parse([-1,{"a":1}]) == 0

    assert parse_hard([1,{"c":"red","b":2},3]) == 4
    assert parse_hard({"d":"red","e":[1,2,3,4],"f":5}) == 0
    assert parse_hard([1,"red",5]) == 6



def easy(data):
    data = json.loads(data)
    return parse(data)


def hard(data):
    data = json.loads(data)
    return parse_hard(data)


test()
data = sys.stdin.read()
print easy(data)
print hard(data)
