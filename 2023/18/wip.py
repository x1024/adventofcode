directions = { 'U': -1j, 'R': 1, 'D': 1j, 'L': -1, }
dirmap = { '0': 'R', '1': 'D', '2': 'L', '3': 'U', }


def main(data, variant=False):
    data = [row.strip() for row in data.split('\n')]
    vert = [] # all vertical lines
    horz = [] # all horizontal lines
    pos = 0 + 0j
    vertices = [pos]
    for row in data:
        dir, n, color = row.split()
        if variant:
            dir = dirmap[color[7]]
            n = int(color[2:2+5], 16)
        start = pos
        end = pos + directions[dir] * int(n)
        pos = end
        vertices.append(end)

        # print(color, n, dir, start, end)
        if start.real > end.real or start.imag > end.imag:
            tmp = start
            start = end
            end = tmp

        if dir in 'UD':
            assert(start.real == end.real)
            vert.append((start, end))
        else:
            assert(start.imag == end.imag)
            horz.append((start, end))

    vert = list(sorted(set(vert), key=lambda v: v[0].real))
    # all y-coordinates of horizontal lines
    h2 = list(sorted(set(h[0].imag for h in horz)))
    set(horz + vert)
    volume = 0
    slices = (
        # all areas with both horizontal and vertical lines in them
        [(x, x) for x in h2] +
        # all areas with only vertical lines in them
        [(h2[i] + 1, h2[i+1] - 1) for i in range(len(h2) - 1)]
    )

    for a,b in slices:
        # for each slice, find all vertical slices that are dug out
        # the result is the total width of the dugout area,
        # multiplied by the height of the slice
        height = b - a + 1
        # relevant vertical lines
        verts = [v[0].real for v in vert if v[0].imag < a and v[1].imag >= b]
        # relevant horizontal lines
        horzs = [(h[0].real, h[1].real) for h in horz if h[0].imag <= a and h[0].imag >= b]
        slices = (
            # A horizontal line is entirely dug out
            horzs +
            # for each two vertical lines,
            # the first one starts a trench and the second one ends it
            [(verts[i], verts[i+1]) for i in range(0, len(verts) - 1, 2)]
        )

        # note that dugout slices may overlap, account for that:
        slices = list(sorted(slices))
        now = slices[0][0]
        for s in slices:
            volume += max(0, s[1] - max(s[0], now) + 1) * height
            now = max(s[1] + 1, now)

    return int(volume)


data_test = open('input-sample.txt', 'r').read().strip()
print(main(data_test))
print(main(data_test, variant=True))

data = open('input.txt', 'r').read().strip()
print(main(data))
print(main(data, variant=True))

