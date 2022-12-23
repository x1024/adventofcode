SIDE_WIDTH = 4

DATA = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

NEIGHBORS = {
  # each line is "neighbor cell, number of clockwise rotations to perform"
  # so if we got "right" on board 1, we'll end up on board 6, with a 180 degree rotation
  1: {
    DOWN: (4, 0),
    UP: (2, 2),
    LEFT: (3, 1),
    RIGHT: (6, 2),
  },
  2: {
    DOWN: (5, 2),
    UP: (1, 2),
    LEFT: (6, 1),
    RIGHT: (3, 0),
  },
  3: {
    DOWN: (5, 1),
    UP: (1, 1),
    LEFT: (2, 0),
    RIGHT: (4, 0),
  },
  4: {
    DOWN: (5, 0),
    UP: (1, 0),
    LEFT: (3, 0),
    RIGHT: (6, 1),
  },
  5: {
    DOWN: (2, 2),
    UP: (4, 0),
    LEFT: (3, 1),
    RIGHT: (6, 0),
  },
  6: {
    DOWN: (2, 3),
    UP: (4, 3),
    LEFT: (5, 0),
    RIGHT: (1, 2),
  }
}

# The position of board X on the input
# (0, 0) means top left
# (0, 1) means to the right of (0, 0)
OFFSETS = [
  (0, 0), # dummy, because boards are [1:6], not [0:5]
  (0, 2),
  (1, 0),
  (1, 1),
  (1, 2),
  (2, 2),
  (2, 3),
]