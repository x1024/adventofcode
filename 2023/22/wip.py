import re


bricks = []
for row in open('input.txt', 'r').read().strip().split("\n"):
    c = list(map(int, re.match(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", row).groups()))
    bricks.append((len(bricks), set((dx, dy, dz)
        for dx in range(c[0], c[3] + 1)
        for dy in range(c[1], c[4] + 1)
        for dz in range(c[2], c[5] + 1))))

def fall(brick): return brick[0], 

def gravity(bricks):
    settled, moved, grid = [], set(), set()

    while bricks:
        falling = []
        for name, blocks in sorted(bricks, key=lambda item: min(b[2] for b in item[1])):
            fallen = set((x,y,z-1) for (x,y,z) in blocks)
            if any(b[2] == 0 for b in fallen) or grid.intersection(fallen):
                settled.append((name, blocks))
                grid.update(blocks)
            else:
                falling.append((name, fallen))
                moved.add(name)
        bricks = falling

    return settled, len(moved)

bricks = gravity(bricks)[0]
fallen = [gravity(bricks[:i] + bricks[i+1:])[1] for i in range(len(bricks))]

print(sum(r == 0 for r in fallen))
print(sum(fallen))
