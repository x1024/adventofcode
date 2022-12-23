import collections

EMPTY = '.'
ELF = '#'

N =  (-1 + 0j)
S =  (+1 + 0j)
W =  (+0 - 1j)
E =  (+0 + 1j)
NW = N + W
NE = N + E
SW = S + W
SE = S + E


class Board(collections.defaultdict):
  ALL_DIRECTIONS = (N, S, W, E, NW, NE, SW, SE)
  DIRECTION_CHECKS = (
    (N, (N, NE, NW)),
    (S, (S, SE, SW)),
    (W, (W, NW, SW)),
    (E, (E, NE, SE)),
  )

  def __init__(self, data):
    super().__init__(lambda: EMPTY, ( 
      (complex(i, j), cell)
      for i, row in enumerate(data.splitlines())
      for j, cell in enumerate(row)
    ))
    self.turn = 0

  def _ranges(self):
    elves = [b for b, v in self.items() if v == ELF]
    minx = int(min(e.real for e in elves))
    maxx = int(max(e.real for e in elves))
    miny = int(min(e.imag for e in elves))
    maxy = int(max(e.imag for e in elves))
    return range(minx, maxx + 1), range(miny, maxy + 1)

  def checksum(self):
    rx, ry = self._ranges()
    return sum(self[complex(x, y)] == EMPTY for x in rx for y in ry)

  def __repr__(self):
    rx, ry = self._ranges()
    board_data = "\n".join(
      (''.join(self[complex(x, y)] for y in ry))
      for x in rx
    )
    return "<Board data={} turn={} checksum={}>".format(board_data, self.turn, self.checksum())

  def elves(self):
    return [pos for pos, value in self.items() if value == ELF]


  def iterate(self):
    to_move = collections.defaultdict(lambda: [])
    moved = 0
    direction_checks = [self.DIRECTION_CHECKS[(self.turn + i) % len(self.DIRECTION_CHECKS)] for i in range(4)]
    for elf in self.elves():
      if all(self[elf + offset] == EMPTY for offset in self.ALL_DIRECTIONS): continue
      new_pos = next((elf + movement for movement, checks in direction_checks
        if all(self[elf + offset] == EMPTY for offset in checks)
      ), None)
      if new_pos is None: continue
      to_move[new_pos].append(elf)

    for new_pos, elves in to_move.items():
      if len(elves) > 1: continue
      self[elves[0]] = EMPTY
      self[new_pos] = ELF
      moved += 1

    self.turn += 1
    return moved


data = open('input.txt', 'r').read().strip()
data_test = '''
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
'''

data_test_2 = '''
.....
..##.
..#..
.....
..##.
.....'''

b = Board(data)
while b.iterate():
  if b.turn <= 10: answer_a = b.checksum()
answer_b = b.turn
print(b)
print(answer_a, answer_b)