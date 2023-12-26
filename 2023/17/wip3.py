import queue

MOD = 1j
MOD = 1000

UP = -1 * MOD
RIGHT = 1
DOWN = 1 * MOD
LEFT = -1
NONE = 0

directions = {
    UP: [LEFT, RIGHT],
    RIGHT: [UP, DOWN],
    DOWN: [LEFT, RIGHT],
    LEFT: [UP, DOWN],
    NONE: [UP, LEFT, DOWN, RIGHT]
}

def dijkstra(minsteps, maxsteps):
    q = queue.PriorityQueue()
    q.put((0, 0, NONE))
    seen = {}
    while not q.empty():
        dist, coord, direction = q.get()
        state = coord, direction

        if state in seen: continue
        seen[state] = dist

        for dir in directions[direction]:
            new_pos = coord
            new_value = dist
            for step in range(1, maxsteps + 1):
                new_pos += dir
                if new_pos not in data: break
                new_value += data[new_pos]
                if step < minsteps: continue
                q.put((new_value, new_pos, dir))

    maxy, maxx = max(x // MOD for x in data), max(x % MOD for x in data)
    return min(seen.get((maxx + maxy * MOD, dir), maxx*maxy*99) for dir in directions)


data = dict((c + r * 1 * MOD, int(col))
    for r, row in enumerate(open('input.txt', 'r').read().strip().split('\n'))
    for c, col in enumerate(row))

print(dijkstra(1, 3))
print(dijkstra(4, 10))

