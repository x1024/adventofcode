#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import json
import pprint


def parse_beacon(row):
    return tuple(map(int, row.split(',')))


def parse_scanner(data):
    rows = data.split("\n")
    return tuple(map(parse_beacon, rows[1:]))


def parse_input(data):
    return tuple(map(parse_scanner, data.split("\n\n")))


permutations = ( 
    ( 0, 1, 2 ),
    ( 0, 2, 1 ),
    ( 1, 0, 2 ),
    ( 1, 2, 0 ),
    ( 2, 0, 1 ),
    ( 2, 1, 0 ),
 )


def get_rotations(beacons):
    result = []
    for beacon in beacons:
        result.append(get_rotations_single(beacon))

    l = len(result[0])
    ret = []
    for i in range(l):
        ret.append(tuple(row[i] for row in result))
    return ret


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
            # print flip, flip0, flip1, flip2, pos_2
            results.append(pos_2)
    return results


def common(r1, r2):
    return len(set(r1).intersection(r2))

def process(beacons):
    beacons = tuple(sorted(beacons))
    m = beacons[0]
    beacons = ((a[0] - m[0], a[1] - m[1], a[2] - m[2])
        for a in beacons)
    beacons = tuple(beacons)
    return beacons, m


def find_common_beacons(scanner_a, scanner_b, limit = 12):
    rot2 = get_rotations(scanner_b)

    for b1 in scanner_a:
        for r2 in rot2:
            for b2 in r2:
                # assume b1 and b2 are the same.
                # Then check if there's enough of a match
                m = (b2[0] - b1[0], b2[1] - b1[1], b2[2] - b1[2])
                r2p = tuple((a[0] - m[0], a[1] - m[1], a[2] - m[2])
                    for a in r2)

                c = common(scanner_a, r2p)
                if c >= limit:
                    common_beacons = tuple(sorted(set(scanner_a + r2p)))
                    return common_beacons, m


def max_offset(offsets):
    relative_offsets = []
    for i in range(len(offsets)):
        oa = offsets[i]
        distance = sum(map(abs, oa))
        # print distance, oa
        relative_offsets.append(distance)

    for i in range(len(offsets)):
        for j in range(i+1, len(offsets)):
            ob = offsets[j]
            ro = ((oa[0] - ob[0]), (oa[1] - ob[1]), (oa[2] - ob[2]))
            distance = sum(map(abs, ro))
            # print distance, ro, oa, ob
            relative_offsets.append(distance)
    return max(relative_offsets)


def solve(data):
    data = parse_input(data)
    cycle = 0
    def optimize(data):
        # print 'optimize', len(data)
        for j in range(1, len(data)):
            print j
            result = find_common_beacons(data[0], data[j])
            if result:
                beacons, offset = result
                data = [row for x, row in enumerate(data) if x != 0 and x != j]
                data.insert(0, beacons)
                # print j, len(data), offset
                # print len(data), offset, len(data[0]), [len(i) for i in data[:4]]
                return data, offset


    offsets = []
    while len(data) > 1:
        data, offset = optimize(data)
        cycle += 1
        offsets.append(offset)
        # print len(data), offset
        # print offset
        # print '--'
        print len(data), len(data[0]), max_offset(offsets)

    # print len(data[0])
    # print max_offset(offsets)
    return len(data[0]), max_offset(offsets)


def easy(data):
    return solve(data)[0]


def hard(data):
    return solve(data)[1]


def test():
    beacons = open('in_test_simple.txt').read()
    beacons = parse_input(beacons)
    rotations = get_rotations(beacons[0])
    assert beacons[0] in rotations
    assert beacons[1] in rotations
    assert beacons[2] in rotations
    assert beacons[3] in rotations
    assert beacons[4] in rotations

    # pprint.pprint(len(rotations))
    # pprint.pprint(len(set(rotations)))
    # pprint.pprint(len(rotations))
    pprint.pprint(rotations[0][0])

    data = open('in_test.txt').read()
    data = parse_input(data)
    offsets = []
    beacons, offset = find_common_beacons(data[0], data[1])
    offsets.append(offset)
    print len(beacons), offset
    beacons, offset = find_common_beacons(beacons, data[4])
    offsets.append(offset)
    print len(beacons), offset
    beacons, offset = find_common_beacons(beacons, data[2])
    offsets.append(offset)
    print len(beacons), offset
    beacons, offset = find_common_beacons(beacons, data[3])
    offsets.append(offset)
    print len(beacons), offset
    print max_offset(offsets)

    data = open('in_test.txt').read()
    # assert easy(data) == 79
    assert hard(data) == 3621


def main():
    test()
    # exit()
    data = open('in.txt').read()
    print easy(data)
    # print hard(data)


if __name__ == '__main__':
    main()