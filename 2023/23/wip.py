import collections
import sys

sys.setrecursionlimit(100000)


def dfs(edges, start, predicate):
    used = set()
    def _dfs(pos, dist):
        used.add(pos)
        if dist > 0 and predicate(pos):
            yield pos, dist
        else:
            for next, d in edges[pos].items():
                if next in used: continue
                yield from _dfs(next, dist + d)
        used.remove(pos)

    yield from _dfs(start, 0)


def main(data, part2=False):
    offsets = { '.': (1, -1, 1j, -1j), 'v': (1j,), '>': (1,), }

    data = data.split('\n')
    grid = collections.defaultdict(lambda: '#', (((c + r * 1j), ('#' if val == '#' else '.') if part2 else val)
        for r, row in enumerate(data) for c, val in enumerate(row)))

    def neighbors(pos): return (offset for offset in offsets[grid[pos]] if grid.get(pos + offset, '#') != '#')
    def is_crossroads(pos): return len(tuple(neighbors(pos))) > 2

    vertices = [p for p,v in grid.items() if v != '#']
    edges = dict((v, dict((v+n, 1) for n in neighbors(v))) for v in vertices)

    # Compress the coordinates
    start, end = 1, len(data[0]) - 1 - 1+ (len(data) - 1) * 1j
    vertices = [start, end] + list(filter(is_crossroads, vertices))
    edges = dict((pos, dict(dfs(edges, pos, lambda v: is_crossroads(v) or v == end))) for pos in vertices)

    return max(d[1] for d in dfs(edges, start, lambda pos: pos == end))


data = open('input.txt', 'r').read().strip()
print(main(data))
print(main(data, part2=True))

