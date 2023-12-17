import functools


def tilt(map, dir=(0 - 1j)):
    for coord, val in reversed(sorted(map.items(), key=lambda x: x[0].real * dir.real + x[0].imag * dir.imag)):
        if val != 'O': continue
        while map.get(coord + dir, None) == '.':
            map[coord] = '.'
            coord += dir
            map[coord] = 'O'
    return map


def value(map):
    rows = int(max(c.real for c in map.keys())) + 1
    return sum(rows - int(coord.imag) for coord, val in map.items() if val == 'O')


board = dict(((c + r * 1j), col)
             for r, row in enumerate(open('input.txt', 'r').read().strip().split('\n'))
             for c, col in enumerate(row))
print(value(tilt(board.copy())))

seen = {}
cycles = 1000000000
while cycles > 0:
    key = tuple(board.items())
    cycles %= seen.get(key, cycles * 2 + 1) - cycles
    seen[key] = cycles
    board = functools.reduce(tilt, ((+0 - 1j), (-1 + 0j), (+0 + 1j), (+1 + 0j)), board)
    cycles -= 1

print(value(board))

