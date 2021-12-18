#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections
import queue


def solve(data):
    data = list(sorted(data.split('\n')))

    storage = collections.defaultdict(lambda: [])
    history = collections.defaultdict(lambda: [])
    operations = collections.defaultdict(lambda: [])
    q = queue.Queue()

    for row in data:
        row = row.split(' ')
        # print row[0]
        if row[0] == 'bot':
            index_operation = 'bot-%s' % (row[1])
            index_low = '%s-%s' % (row[5], row[6])
            index_high = '%s-%s' % (row[10], row[11])
            operations[index_operation] = [index_low, index_high]
        else:
            value = int(row[1])
            index_bot = 'bot-%s' % (row[5])
            storage[index_bot].append(value)
            q.put(index_bot)

        while not q.empty():
            index = q.get()
            if index.startswith('bot') and len(storage[index]) == 2:
                low, high = sorted(storage[index])
                index_low, index_high = operations[index]
                storage[index_low].append(low)
                storage[index_high].append(high)
                storage[index] = []
                history[index].append((low, high))
                q.put(index_low)
                q.put(index_high)

    return storage, history


def easy(data, pair = (17, 61)):
    _, history = solve(data)
    pair = tuple(sorted(pair))
    for row, values in history.items():
        if pair in values:
            return int(row.split('-')[-1])


def hard(data):
    storage, history = solve(data)
    return storage['output-0'][0] * storage['output-1'][0] * storage['output-2'][0]


def test():
    data = '''value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2'''
    expected = {
        'output-0': [ 5 ],
        'output-1': [ 2 ],
        'output-2': [ 3 ],
    }
    actual = solve(data)[0]
    for i in expected:
        assert actual[i] == expected[i]

    assert easy(data, (2, 5)) == 2


if __name__ == '__main__':
    test()
    data = sys.stdin.read()
    print easy(data)
    print hard(data)
