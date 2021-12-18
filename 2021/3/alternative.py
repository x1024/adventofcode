#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def get_common_bit(bit, rows):
    return int(sum(row[bit] for row in rows) * 2 / len(rows))


def bin2int(bits):
    return int(''.join(map(str, bits)), 2)


def easy(rows):
    gamma = bin2int(get_common_bit(bit, rows) for bit in range(len(rows[0])))
    return gamma * (gamma ^ (2**(len(rows[0])) - 1))


def hard(rows):
    def filter_rows(rows, comparison):
        for bit in range(0, len(rows[0])):
            rows = [row for row in rows if comparison(row[bit], get_common_bit(bit, rows))]
            if len(rows) == 1:
                return bin2int(rows[0])

    return filter_rows(rows, lambda a, b: a == b) * filter_rows(rows, lambda a, b: a != b)


data = [map(int, row.strip()) for row in open('in.txt').read().strip('\n').split('\n')]
print easy(data)
print hard(data)
