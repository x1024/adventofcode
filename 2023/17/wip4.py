from dataclasses import dataclass, field
from typing import Any
from typing import NamedTuple
import queue

MOD = 1j

UP = -1j
RIGHT = 1
DOWN = 1j
LEFT = -1
NONE = 0

directions = {
    UP: [LEFT, RIGHT],
    RIGHT: [UP, DOWN],
    DOWN: [LEFT, RIGHT],
    LEFT: [UP, DOWN],
    NONE: [UP, DOWN, LEFT, RIGHT]
}

@dataclass(order=True)
class State():
    dist: int
    coord: Any=field(compare=False)
    direction: Any=field(compare=False)


def dijkstra(steps):
    q = queue.PriorityQueue()
    q.put(State(0, 0, NONE))
    seen = {}
    while not q.empty():
        s = q.get()
        dist, coord, direction = s.dist, s.coord, s.direction
        pos = (coord, direction)
        if pos in seen: continue
        seen[pos] = dist

        for dir in directions[direction]:
            for step in steps:
                new_pos = coord + dir * step
                if new_pos not in data: continue
                new_value = dist + sum(data[coord + dir * s] for s in range(1, step+1))
                q.put(State(new_value, new_pos, dir))

    maxy, maxx = int(max(x.imag for x in data)), int(max(x.real for x in data))
    return min(seen.get((maxx, maxy, dir), maxx*maxy*99) for dir in directions)


data = dict((c + r * 1j, int(col))
    for r, row in enumerate(open('input-sample.txt', 'r').read().strip().split('\n'))
    for c, col in enumerate(row))

print(dijkstra(range(1, 3 + 1)))
# print(dijkstra(range(4, 10 + 1)))
