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
    UP: (0, -1),
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
}

def dijkstra(minsteps, maxsteps):
    q = queue.PriorityQueue()
    q.put((0, (0, 0, NONE)))
    seen = {}
    maxx, maxy = len(data), len(data[0])
    maxval = maxx * maxy * 99

    while not q.empty():
        dist, pos = q.get()
        x, y, direction = pos

        if pos in seen: continue
        seen[pos] = dist

        for dir, (dx, dy) in directions.items():
            if dir == opposite[direction]: continue
            if dir == direction: continue
            new_value = dist
            nx, ny = x, y
            for step in range(1, maxsteps + 1):
                nx += dx
                ny += dy
                if not (0 <= nx < maxx and 0 <= ny < maxy): break
                new_value += data[nx][ny]
                if step < minsteps: continue
                new_pos = (nx, ny, dir)
                if seen.get(new_pos, maxval) <= new_value: continue
                q.put((new_value, new_pos))

    return min(seen.get((maxx-1, maxy-1, dir), maxval) for dir in directions)


data = [
    list(map(int, row))
    for r, row in enumerate(open('input.txt', 'r').read().strip().split('\n'))
]

print(dijkstra(1, 3))
print(dijkstra(4, 10))
