import collections
import functools

data = dict(((c + r * 1j), col)
    for r, row in enumerate(open('input.txt', 'r').read().strip().split('\n'))
    for c, col in enumerate(row))

start = (x for x in data if data[x] == 'S').__next__()
maxx = max(data.keys(), key=lambda x: x.real).real
maxy = max(data.keys(), key=lambda x: x.imag).imag * 1j
straights = ( (0 + start.imag * 1j), (maxx + start.imag * 1j), (start.real + 0j), (start.real + maxy),)
diagonals = ( (0 + 0j), (maxx + 0j), (0 + maxy), (maxx + maxy),)
width = maxx + 1


def bfs(start, limit):
    limit = min(limit, maxx * 2 + limit % 2)
    return _bfs(start, limit)

@functools.lru_cache(maxsize=None)
def _bfs(start, limit):
    if limit < 0: return 0
    queue, seen = collections.deque([(0, start)]), set([(0, start)])
    while queue:
        steps, x = queue.popleft()
        if steps == limit: continue
        for x2 in ( x + 1, x - 1, x + 1j, x - 1j ):
            if data.get(x2, '#') == '#': continue
            s2 = ((steps + 1) % 2, x2)
            if s2 in seen: continue
            queue.append((steps + 1, x2))
            seen.add(s2)
    return sum(1 for a,s in seen if a % 2 == limit % 2)


def main(steps):
    return (
        bfs(start, steps) +
        sum(bfs(pos, steps - 1 - (offset - 1) * width - width // 2) * 1
            for pos in straights
            for offset in range(1, int(steps // width) + 2)) + 
        sum(bfs(pos, steps - 1 - (offset - 1) * width) * (offset - 1)
            for pos in diagonals
            for offset in range(1, int(steps // width) + 2))
    )


# print(main(64))
print(main(26501365))
n = 26501365 // 262 + 1
print(62312 * n**2 - 93248 * n + 34893)
