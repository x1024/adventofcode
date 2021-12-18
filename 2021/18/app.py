#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import json


def parse_input(data):
    return map(json.loads, data.split("\n"))


def increment_successor(path):
    pass


def find(number, path, callback):
    if len(path) == 0:
        return callback(number)
    if path[0] == 0:
        return find(number[0], path[1:], callback)
    else:
        return find(number[1], path[1:], callback)


def explode(number, depth = 0, path = tuple()):
    # print 'asd', number, depth, path

    if type(number) == int:
        return False, number, None

    if depth == 4:
        return True, 0, [ path, number ]

    a, b = number
    result, new_number, info = explode(a, depth + 1, path + (0,))
    if result:
        return True, [new_number, b], info

    result, new_number, info = explode(b, depth + 1, path + (1,))
    if result:
        return True, [a, new_number], info

    return False, [a, b], None

def get_paths(number, path = tuple()):
    # print number, path
    if type(number) == int:
        yield path
        return

    for p in get_paths(number[0], path + (0,)):
        yield p
    for p in get_paths(number[1], path + (1,)):
        yield p


def increment(number, path, value):
    if len(path) == 0:
        return number + value
    if path[0] == 0:
        val = increment(number[0], path[1:], value)
        return [val, number[1]]
    else:
        val = increment(number[1], path[1:], value)
        return [number[0], val]


def do_explode(number):
    result, new_number, info = explode(number)
    paths = list(get_paths(new_number))
    number = new_number

    if result:
        path, to_increment = info
        i = paths.index(path)

        if i > 0:
            p2 = paths[i-1]
            number = increment(number, p2, to_increment[0])

        if i < len(paths) - 1:
            p2 = paths[i+1]
            number = increment(number, p2, to_increment[1])

    return number

def split(number):
    a, b = number
    if type(a) == int:
        if a >= 10:
            a = [a // 2, a // 2 + a % 2]
            return True, [a, b]
    else:
        result, new_number = split(a)
        a = new_number
        if result: return True, [a, b]

    if type(number[1]) == int:
        if b >= 10:
            b = [b // 2, b // 2 + b % 2]
            return True, [a, b]
    else:
        result, new_number = split(b)
        b = new_number
        if result: return True, [a, b]

    return False, [a, b]


def magnitude(number):
    if type(number) == int:
        return number
    return 3 * magnitude(number[0]) + 2 * magnitude(number[1])


def add_numbers(numbers):
    return reduce(lambda a, b: reduce_number([a, b]), numbers)


def reduce_number(data):
    while True:
        new_data = do_explode(data)
        if data == new_data:
            _, new_data = split(data)
            if data == new_data:
                break
        data = new_data
    return data


def easy(data):
    data = parse_input(data)
    return magnitude(add_numbers(data))


def hard(data):
    data = parse_input(data)
    ranges = [(i, j) for i in range(len(data)) for j in range(len(data)) if i != j]
    numbers = [(data[i], data[j]) for (i, j) in ranges]
    numbers = map(reduce_number, numbers)
    numbers = map(magnitude, numbers)
    return max(numbers)


def test():
    assert do_explode([[[[[9, 8], 1], 2], 3], 4]) == [[[[0, 9], 2], 3], 4]
    assert do_explode([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
    assert do_explode([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
    assert do_explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    assert do_explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

    assert add_numbers([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]) == [
        [[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]


    assert add_numbers([
        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
        [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
        [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
        [7,[5,[[3,8],[1,4]]]],
        [[2,[2,2]],[8,[8,1]]],
        [2,9],
        [1,[[[9,3],9],[[9,0],[0,7]]]],
        [[[5,[7,4]],7],1],
        [[[[4,2],2],6],[8,7]],
    ]) == [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]

    assert magnitude([[1, 2], [[3, 4], 5]]) == 143
    assert magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == 1384
    assert magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == 445
    assert magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]) == 791
    assert magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]) == 1137
    assert magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]) == 3488

    data = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''
    assert easy(data) == 4140
    assert hard(data) == 3993


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()
