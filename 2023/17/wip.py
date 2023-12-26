import queue

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
NONE = -1

opposite = {
    UP: DOWN,
    RIGHT: LEFT,
    DOWN: UP,
    LEFT: RIGHT,
    NONE: NONE,
}

directions = {
    UP: -1j,
    RIGHT: 1,
    DOWN: 1j,
    LEFT: -1,
}

def dijkstra(steps):
    q = queue.PriorityQueue()
    q.put((0, (0, 0, NONE)))
    seen = {}
    while not q.empty():
        dist, pos = q.get()
        x, y, direction = pos
        coord = x + y * 1j

        if pos in seen: continue
        seen[pos] = dist

        for dir, offset in directions.items():
            if dir == opposite[direction]: continue
            if dir == direction: continue
            for step in steps:
                new_pos = coord + offset * step
                if new_pos not in data: continue
                new_value = dist + sum(data[coord + offset * s] for s in range(1, step+1))
                q.put((new_value, (int(new_pos.real), int(new_pos.imag), dir)))

    maxy, maxx = int(max(x.imag for x in data)), int(max(x.real for x in data))
    return min(seen.get((maxx, maxy, dir), maxx*maxy*99) for dir in directions)


data = dict((c + r * 1j, int(col))
    for r, row in enumerate(open('input.txt', 'r').read().strip().split('\n'))
    for c, col in enumerate(row))

print(dijkstra(range(1, 3 + 1)))
print(dijkstra(range(4, 10 + 1)))
