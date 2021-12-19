#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import queue

permutations = (( 0, 1, 2 ), ( 0, 2, 1 ), ( 1, 0, 2 ), ( 1, 2, 0 ), ( 2, 0, 1 ), ( 2, 1, 0 ))


def parse_beacon(row): return tuple(map(int, row.split(',')))
def parse_scanner(data): return tuple(map(parse_beacon, data.split("\n")[1:]))
def parse_input(data): return list(map(parse_scanner, data.split("\n\n")))


def get_rotations(beacons):
    result = tuple(get_rotations_single(beacon) for beacon in beacons)
    return tuple(tuple(row[i] for row in result)
        for i in range(len(result[0])))


def get_rotations_single(pos):
    # flips = int(2 ** len(pos))
    flips = 8
    results = []
    for p in permutations:
        pos_1 = (
            pos[p[0]], 
            pos[p[1]], 
            pos[p[2]]
        )
        for flip in range(flips):
            flip0 = -1 if (flip & 1) else 1
            flip1 = -1 if (flip & 2) else 1
            flip2 = -1 if (flip & 4) else 1
            pos_2 = (
                pos_1[0] * flip0,
                pos_1[1] * flip1,
                pos_1[2] * flip2,
            )
            results.append(pos_2)
    return results


def subtract_point(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])


def add_point(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1], p1[2] + p2[2])


def find_common_beacons(beacons_a, beacons_b, limit = 12):
    # scanner_a has a position,
    # scanner_b does not have a position
    # scanner_a coordinates are absolute
    # scanner_b coordinates are relative

    beacons_a = set(beacons_a)
    for beacons_rotated in get_rotations(beacons_b):
        for b2 in beacons_rotated:
            for b1 in beacons_a:
                # assume b1 and b2 are the same.
                # Then check if there's enough of a match
                offset = subtract_point(b1, b2)
                beacons_rotated_absolute = tuple(add_point(a, offset) for a in beacons_rotated)
                common = beacons_a.union(beacons_rotated_absolute)

                if len(beacons_a) + len(beacons_rotated) - len(common) >= limit:
                    return beacons_rotated_absolute, offset
                    # This is an order of magnitude slower, but it's actually correct:
                    # return common, offset

                    # Note: the "Real" solution would require us to merge the points
                    # every time we join two regions.
                    # Suppose we have regions A, B, C
                    # Each of the regions A and B might not have 12 common points with C
                    # - but the union A+B might have them.

                    # Example:
                    # Clearly, A & B have 12 common points and can be merged
                    # However, C doesn't have 12 common points with either A or B.
                    # A merge cannot happen
                    # But, C has 12 common points with the union (A+B).
                    # Therefore, in the general case we would have to merge every 2 scanners that we match
                    #            ---------------------
                    #            |        C          |
                    #            |                   |
                    #            |                   |
                    #            |                   |
                    #     ---------------------      |     
                    #     |      |  ....  |----------|--------|
                    #     |      |  ....  |   | .... |        |
                    #     |      --------------------|        |
                    #     |               |...|               |
                    #     |  A            |...|            B  |
                    #     |               |...|               |
                    #     |               |...|               |
                    #     |               |   |               |
                    #     ----------------|----               |
                    #                     ---------------------
                    # return common, offset


def max_offset(offsets):
    return max(
        # get all relative offsets between each pair of scanners
        sum(map(abs, subtract_point(oa, ob)))
        for oa in offsets
        for ob in offsets
        if oa != ob
    )


def solve(data):
    beacons = parse_input(data)
    scanners = [None] * len(beacons) # scanners have no fixed positions at first
    scanners[0] = (0, 0, 0) # The first scanner is assumed to be at (0, 0, 0)

    q = queue.Queue()
    q.put(0)
    while not q.empty():
        i = q.get()
        for j in range(len(beacons)):
            if i == j or scanners[j]: continue
            result = find_common_beacons(beacons[i], beacons[j])
            if not result: continue
            beacons[j] = result[0]
            scanners[j] = result[1]
            print >>sys.stderr, "found match:", (i, j), sum(map(bool, scanners))
            q.put(j)

    beacons = set(sum(beacons, tuple()))
    return len(beacons), max_offset(scanners)


def test():
    data = open('in_test.txt').read()
    assert solve(data) == (79, 3621)


def main():
    test()
    data = open('in.txt').read()
    answer_easy, answer_hard = solve(data)
    print answer_easy
    print answer_hard


if __name__ == '__main__':
    main()