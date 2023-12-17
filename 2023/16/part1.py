import collections
import numpy
import pprint
import re
import functools
import itertools

def rotate_left(pos):
    return (int(pos.imag) + int(pos.real) * 1j)

def rotate_right(pos):
    return (-int(pos.imag) + int(-pos.real) * 1j)

'''
 0  1 => -1 0
 1  0 => 0 -1
 0 -1 => 1 0
-1  0 => 0 1
'''


def main(data):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split('\n')]
    # data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))

    # parse into a grid
    map = {}
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            coord = (c + r * 1j)
            map[coord] = col
    seen = set()
    seen2 = set()

    result = 0
    def spread_beam(beam):
        # print("spread_beam", beam)
        while True:
            pos, dir = beam
            tile = map.get(pos, None)
            # print(tile, "      ", beam, tile)
            if not tile: return
            if beam in seen2: return
            seen.add(pos)
            seen2.add(beam)
            if tile == '|':
                # print("split 1", pos, dir)
                if dir.real != 0:
                    spread_beam((pos + 1j, (0 + 1j)))
                    spread_beam((pos - 1j, (0 - 1j)))
                    return
            elif tile == '-':
                # print("split 2", pos, dir)
                if dir.imag != 0:
                    spread_beam((pos + 1, (+1 + 0j)))
                    spread_beam((pos - 1, (-1 - 0j)))
                    return
            elif tile == '\\':
                print("ROTATE")
                dir = rotate_left(dir)
            elif tile == '/':
                print("ROTATE LEFT", dir, " ", end='')
                dir = rotate_right(dir)
                print(dir)
            elif tile == '.':
                pass
            else:
                print("BAD TILE", tile)
                raise "BAD TILE"
            print(pos, dir, dir)
            beam = (pos + dir, dir)

    beam = ((0 + 0j), (1 + 0j))
    spread_beam(beam)
    return (len(seen))

    for r, row in enumerate(data):
        for c, col in enumerate(row):
            coord = (c + r * 1j)
            if coord in seen:
                print("#", end='')
            else:
                print(col, end='')
        print()




    print(result)
    return result


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
