import functools


# Takes a point and transforms it according to a mapping.
# If the point isn't in any of the segments, returns the point unchanged
def transform(value, mapping):
    return next((d + value for d, s, e in mapping if s <= value <= e), value)


# Takes a range and transforms it according to a mapping
# Since the mapping can be non-linear, returns a list of non-overlapping ranges
# that cover the same values as the original range.
def transform_range(rng, mapping):
    # Take all unique "interesting points"
    # (start and end of each segment, and the start and end of the range)
    points = [s for d,s,e in mapping] + [e for d,s,e in mapping]
    points = [c for c in points if c >= rng[0] and c <= rng[1]]
    points += [rng[0], rng[1]]
    points = list(sorted(set(points)))

    # Form ranges between each two consecutive interesting points
    # Note that the ranges are [a,b] (inclusive on both ends)
    # Transform each of the new ranges (the mapping is linear within each segment)
    tr = functools.partial(transform, mapping=mapping)
    return list(zip(map(tr, points), map(tr, (c - 1 for c in points[1:]))))


def main(data):
    [seeds, *map_defs] = [row.strip() for row in data.split('\n\n')]
    seeds = list(map(int, seeds.replace("seeds: ", "").split(" ")))
    maps = [[list(map(int, row.split(" "))) for row in game.split("\n")[1:]] for game in map_defs]
    # Transform from (destination, start, length) to (destination_offset, start, end)
    maps = [sorted( (d - s, s, s+l - 1) for d, s, l in m ) for m in maps]

    yield min(functools.reduce(transform, maps, seed) for seed in seeds)

    seed_ranges = zip(seeds[::2], (seeds[x] + seeds[x+1] - 1 for x in range(0, len(seeds), 2)))
    yield min(functools.reduce(
        # Turn each range into a list of non-overlapping transformed ranges,
        # according to the mapping. Flatten the list.
        lambda ranges, mapping: sum(
            (transform_range(rng, mapping) for rng in ranges),
        []),
        maps,
        seed_ranges
    ))[0]


print(*main(open('input-sample.txt', 'r').read().strip()))
print(*main(open('input.txt', 'r').read().strip()))
