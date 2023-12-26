import collections
import numpy
import pprint
import re
import functools
import itertools


def main(data):
    bricks = []
    bricks_blocks = []
    for row in data.split("\n"):
        g = re.match(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", row)
        x, y, z, x1, y1, z1 = g.groups()
        start = [
            min(int(x), int(x1)),
            min(int(y), int(y1)),
            min(int(z), int(z1))
        ]
        end = [
            max(int(x), int(x1)),
            max(int(y), int(y1)),
            max(int(z), int(z1))
        ]

        blocks = []
        for dx in range(start[0], end[0] + 1):
            for dy in range(start[1], end[1] + 1):
                for dz in range(start[2], end[2] + 1):
                    blocks.append((dx, dy, dz))
        bricks_blocks.append((row, set(blocks)))
        bricks.append((start, end, len(bricks)))

    bricks_blocks = list(sorted(bricks_blocks, key=lambda item: min(b[2] for b in item[1])))

    def can_fall(brick, done):
        name, blocks = brick
        blocks = set((x,y,z-1) for (x,y,z) in blocks)
        if any(z == 0 for _,_,z in blocks): return False
        if any(blocks.intersection(dbirck[1]) for dbirck in done): return False
        return True

    def fall_blocks(bricks, count=False):
        time = 0

        done = []
        fallen = set()
        while len(bricks) > 0:
            bricks = list(sorted(bricks, key=lambda item: min(b[2] for b in item[1])))
            not_done = []
            for brick in bricks:
                if can_fall(brick, done):
                    name, blocks = brick
                    blocks = set((x,y,z-1) for (x,y,z) in blocks)
                    brick = (name, blocks)
                    not_done.append(brick)
                    fallen.add(brick[0])
                else:
                    done.append(brick)

            bricks = not_done
            if len(bricks) == 0: break
            time += 1
        return time, done, fallen

    time, done, fallen = fall_blocks(bricks_blocks)
    bricks = done

    res = 0
    res2 = 0
    for i in range(0, len(bricks)):
        temp = bricks[:i] + bricks[i+1:]
        f = fall_blocks(temp, count=True)
        print(i, len(temp), f[0], len(f[2]))
        if f[0] == 0:
            res += 1
        res2 += len(f[2])
        # print(len(bricks))
    return res, res2
    exit()


data_test = open('input-sample.txt', 'r').read().strip()
result = main(data_test)
print("Test Result: {}".format(result))

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
