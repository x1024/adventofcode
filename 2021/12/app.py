#!/usr/bin/env python
#-*- coding: UTF-8 -*-

NODE_START = 'start'
NODE_END = 'end'
DOUBLES_DISABLED = -1


def parse_input(data):
    rows = data.split('\n')
    nodes = {}
    for row in rows:
        a, b = row.split('-')
        la = nodes.get(a, [])
        if b != NODE_START: la.append(b)
        nodes[a] = la
        lb = nodes.get(b, [])
        if a != NODE_START: lb.append(a)
        nodes[b] = lb
    return nodes


def solve(nodes, use_doubles=False):
    def _solve(current, double, path):
        if current == NODE_END: return [path + [current]]
        if current in path and current.lower() == current:
            if ((not use_doubles) or double is not None): return []
            double = current
        return sum((_solve(node, double, path + [current]) for node in nodes[current]), [])
    return len(_solve(NODE_START, None, []))

 
def easy(data):
    return solve(parse_input(data))


def hard(data):
    return solve(parse_input(data), use_doubles=True)



def test():
    data = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''
    assert easy(data) == 10
    assert hard(data) == 36

    data = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''

    assert easy(data) == 19
    assert hard(data) == 103

    data = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''
    assert easy(data) == 226
    assert hard(data) == 3509


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

