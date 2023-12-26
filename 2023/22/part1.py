import collections
import numpy
import pprint
import re
import functools
import itertools


def main(data):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    bricks = []
    bricks_blocks = []
    for row in data:
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
        bricks_blocks.append(set(blocks))
        bricks.append((start, end, len(bricks)))

    asd = bricks_blocks[0]
    bricks_blocks = list(sorted(bricks_blocks, key=lambda item: min(b[2] for b in item)))

    def fall_blocks(bricks, limit=999999):
        time = 0
        def can_fall(brick):
            brick = set((x,y,z-1) for x,y,z in brick)
            if any(z == 0 for _,_,z in brick): return False
            if any(brick.intersection(dbirck) for dbirck in done): return False
            return True

        done = []
        while len(bricks) > 0:
            bricks = list(sorted(bricks, key=lambda item: min(b[2] for b in item)))
            not_done = []
            for brick in bricks:
                if can_fall(brick):
                    brick = set((x,y,z-1) for x,y,z in brick)
                    not_done.append(brick)
                else:
                    done.append(brick)

            bricks = not_done
            if len(bricks) == 0: break
            time += 1
        return time, done

    time, done = fall_blocks(bricks_blocks)
    bricks = done
    print("DONE")
    for z in range(9, 0, -1):
        print(z, end=' ')
        for y in range(0, 10):
            for b in bricks:
                if any(z == z1 and y == y1 for x1, y1, z1 in b):
                    print('#', end='')
                    break
            else:
                print(".", end='')
        print()

    print()
    for z in range(9, 0, -1):
        print(z, end=' ')
        for x in range(0, 10):
            for b in bricks:
                if any(z == z1 and x == x1 for x1, y1, z1 in b):
                    print('#', end='')
                    break
            else:
                print(".", end='')
        print()

    print()

    res = 0
    for i in range(0, len(bricks)):
        temp = bricks[:i] + bricks[i+1:]
        f = fall_blocks(temp, 1)
        print(i, len(temp), f[0])
        if f[0] == 0:
            res += 1
        # print(len(bricks))
    return res
    exit()


data_test = open('input-sample.txt', 'r').read().strip()
result = main(data_test)
print("Test Result: {}".format(result))

# exit()

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
