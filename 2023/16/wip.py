import itertools
import functools
import collections

paths = {
    '|' : lambda dir: (1j,-1j),
    '-' : lambda dir: (1,-1),
    '\\' : lambda dir: (int(dir.imag) + int(dir.real) * 1j,),
    '/' : lambda dir: (-int(dir.imag) + int(-dir.real) * 1j,),
    '.' : lambda dir: (dir, ),
    None: lambda dir: tuple(),
}
data = [row.strip() for row in open('input.txt', 'r').read().strip().split('\n')]
data = collections.defaultdict(lambda: None, (((c + r * 1j), col) for r, row in enumerate(data) for c, col in enumerate(row)))
maxx, maxy = max(x.imag for x in data), max(x.real for x in data)


def solve(start):
    q, seen = [start], set()
    while q:
        pos, dir = cur = q.pop()
        q += [(pos + d, d) for d in paths[data[pos]](dir) if (pos + d, d) not in seen]
        seen.add(cur)
    return len(set(pos for pos, _ in seen if data[pos]))


print(solve((0, 1)))
print(max(map(solve, itertools.product(
    filter(lambda c: c.imag in (0, maxy) or c.real in (0, maxx), data),
    (1, -1, 1j, -1j)
))))
