#!/usr/bin/env python
#-*- coding: UTF-8 -*-


import queue
import md5


memo = {}
def get_hash(data, stretch):
    key = (data, stretch)
    val = memo.get(key, None)
    if not val:
        val = md5.md5(data).hexdigest()
        while stretch > 0:
            val = md5.md5(val).hexdigest()
            stretch -= 1
        memo[key] = val
    return val


NUM_CHARS = 16
chars = [str(hex(i))[2:] for i in range(NUM_CHARS)]
triples = [c*3 for c in chars]
quadruples = [c*4 for c in chars]
quintuples = [c*5 for c in chars]
sextuples = [c*6 for c in chars]


def check(seed, stretch, i):
    hash = get_hash("%s%s" % (seed, i), stretch)

    found = [(hash.find(triples[i1]), i1) for i1 in range(NUM_CHARS)]
    found = [(a, b) for (a, b) in found if a >= 0]
    if not found: return False

    i1 = min(found)[1]
    # print 'found', i, i1, hash
    t = triples[i1]
    q = quintuples[i1]
    for j in range(1000):
        hash2 = get_hash("%s%s" % (seed, i + 1 + j), stretch)
        if q in hash2:
            # print 'hash!', i, i + 1 + j, t, q, hash, hash2
            return True
    return False



def solve(seed, stretch = 0, num_hashes = 64):
    i = 0
    while True:
        num_hashes -= check(seed, stretch, i)
        if not num_hashes: return i
        i += 1

def easy(seed):
    return solve(seed)


def hard(seed):
    return solve(seed, 2016)


def test():
    assert easy('abc') == 22728


if __name__ == '__main__':
    test()
    # data = sys.stdin.read()
    key = 'ihaygndm'
    print easy(key)
    print hard(key)