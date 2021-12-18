#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import json
import anytree


def create_tree(row, parent=None):
    if type(row) == int: return anytree.Node(row, parent=parent)
    p = anytree.Node('_', parent=parent)
    create_tree(row[0], parent=p)
    create_tree(row[1], parent=p)
    return p


def parse_input(data):
    data = map(json.loads, data.split("\n"))
    data = map(create_tree, data)
    return data


def explode(tree):
    _last = None
    iterator = anytree.PreOrderIter(tree)
    for node in iterator:
        if type(node.name) == int: _last = node
        elif node.depth == 4:
            child1 = next(iterator)
            child2 = next(iterator)
            _next = next((n for n in iterator if type(n.name) == int), None)
            if _last: _last.name += child1.name
            if _next: _next.name += child2.name
            node.children = []
            node.name = 0
            return True
    return False


def split(tree):
    for i in anytree.PreOrderIter(tree):
        if type(i.name) == int and i.name >= 10:
            i.children = [anytree.Node(i.name // 2), anytree.Node(i.name - i.name // 2)]
            i.name = '_'
            return True
    return False


def magnitude(tree):
    if type(tree.name) == int: return tree.name
    return 3 * magnitude(tree.children[0]) + 2 * magnitude(tree.children[1])


def add_numbers(a, b):
    number = anytree.Node('_', children=[a, b])
    while explode(number) or split(number): continue
    return number


def copy_tree(root, parent=None):
    new_root = anytree.Node(root.name, parent=parent)
    for child in root.children: copy_tree(child, new_root)
    return new_root


def easy(data):
    return magnitude(reduce(add_numbers, parse_input(data)))


def hard(data):
    data = parse_input(data)
    ranges = [(i, j) for i in range(len(data)) for j in range(len(data)) if i != j]
    numbers = [add_numbers(copy_tree(data[i]), copy_tree(data[j])) for (i, j) in ranges]
    return max(map(magnitude, numbers))


def test():
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
