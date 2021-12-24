#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def parse_input(data):
    data = [row.strip().split(" ") for row in data.split("\n") if row]
    offsets_x = [int(c[5][2]) for c in chunks(data, 18)]
    offsets_x = [x if x < 10 else 0 for x in offsets_x]
    offsets_y = [int(c[15][2]) for c in chunks(data, 18)]
    return offsets_x, offsets_y


def generator(l, reverse=False):
    '''
    Returns all numbers of length l, with no zeroes in them.
    '''
    data = [0] * l
    r = range(9, 0, -1) if reverse else range(1, 10)

    def _generator(i):
        if i == l:
            yield tuple(data)
            return
        for j in r:
            data[i] = j
            for k in _generator(i + 1):
                yield k

    return _generator(0)


def program(data, offsets_x, offsets_y):
    z = 0
    index = 0
    result = []

    for i in range(len(offsets_x)):
        if offsets_x[i] >= 0:
            w = int(data[index])
            index += 1
            z = z * 26 + w + offsets_y[i]
            digit = w
        else:
            x = (z % 26) + offsets_x[i]
            z = int(z / 26)
            digit = x
            if not (1 <= digit <= 9): return False
        result.append(digit)
  
    return ''.join(map(str, result))


def solve(data, reverse=False):
    offsets_x, offsets_y = parse_input(data)
    independent_numbers = sum(1 if x == 0 else 0 for x in offsets_x)
    results = (program(i, offsets_x, offsets_y)
        for i in generator(independent_numbers, reverse=reverse))
    return next(r for r in results if r)


def easy(data): return solve(data)
def hard(data): return solve(data, reverse=True)


def main():
    data = open('in.txt', 'r').read()
    print easy(data)
    print hard(data)
    


if __name__ == '__main__':
    main()