import functools


def transform(value, mapping):
    return next((d + value - s for d, s, l in mapping if s <= value < s + l), value)


def transform_range(rng, mapping):
    points = [s for d,s,l in mapping] + [s+l for d,s,l in mapping]
    points = [c for c in points if c >= rng[0] and c < rng[0] + rng[1]]
    points += [rng[0], rng[0] + rng[1]]
    points = list(sorted(set(points)))

    left = map(lambda c: transform(c, mapping), points)
    right = map(lambda c: transform(c - 1, mapping) + 1, points[1:])
    return [(a, b - a) for a, b in zip(left, right)]


def main(data):
    [seeds, *map_defs] = [row.strip() for row in data.split('\n\n')]
    seeds = list(map(int, seeds.replace("seeds: ", "").split(" ")))
    seed_ranges = zip(seeds[::2], seeds[1::2])
    maps = [[list(map(int, row.split(" "))) for row in game.split("\n")[1:]] for game in map_defs]

    yield min(functools.reduce(transform, maps, seed) for seed in seeds)
    yield min(functools.reduce(lambda ranges, mapping: sum((transform_range(rng, mapping) for rng in ranges), []), maps, seed_ranges))[0]


print(*main(open('input-sample.txt', 'r').read().strip()))
print(*main(open('input.txt', 'r').read().strip()))

