#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import queue
import md5

# doors are: up, down, left, right - in this order
open_doors = 'bcdef'
offsets = [
    (0, -1),
    (0, +1),
    (-1, 0),
    (+1, 0),
]
direction_names = 'UDLR'
directions = list(enumerate(offsets))


memo = {}
def doors(seed, path):
    key = seed + path
    state = memo.get(key, None)
    if not state:
        hash = md5.md5(key).hexdigest()[:4]
        state = [c in open_doors for c in hash]
        memo[key] = state
    return state


def solve(seed, return_longest=False):
    size = 4
    start = (0, 0)
    end = (size - 1, size - 1)

    q = queue.Queue()
    q.put((start, ''))
    last_solution = None
    while not q.empty():
        pos, path = q.get()
        door_state = doors(seed, path)
        if pos == end:
            if return_longest:
                last_solution = path
                continue
            else:
                return path

        for index, offset in directions:
            if not door_state[index]: continue
            new_pos = (pos[0] + offset[0], pos[1] + offset[1])

            if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= size or new_pos[1] >= size: continue

            q.put((new_pos, path + direction_names[index]))

    return len(last_solution)


def easy(data):
    return solve(data)


def hard(data):
    return solve(data, return_longest=True)


def test():
    assert easy('ihgpwlah') == 'DDRRRD'
    assert easy('kglvqrro') == 'DDUDRLRRUDRD'
    assert easy('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'

    assert hard('ihgpwlah') == 370
    assert hard('kglvqrro') == 492
    assert hard('ulqzkmiv') == 830


if __name__ == '__main__':
    test()
    data = 'udskfozm'
    print easy(data)
    print hard(data)