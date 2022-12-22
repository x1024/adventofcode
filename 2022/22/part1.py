import IPython
import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read()

data_test = '''        ...#
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

data = '''                                                  ....#....................#..#..............#.#.............#............#.........#..........#......
                                                  ................#......#...#........#.#.....#...#....#..........#.......................#........#.#
                                                  ..........##.........#....................###..##.......#...#......#.......#.................#......
                                                  ........#....##...........##.........................#........................#..........#.......#..
                                                  ...##................#..........#......#........#........#..............#.................#.........
                                                  ................#..............#.....#....#..#....................##......#.........................
                                                  ......#................##........................#..#.#..........#.......#...........#......#.......
                                                  ..#........................#.......#.............#...#....................#................#........
                                                  ............#..............#.#...........#......................................##.#................
                                                  ......#..#............#..#.#..#........#....#..#....#............#...............#...#..............
                                                  ............#..........#..........#.#.#............#...............#...............#....##....#.....
                                                  .....#............#...........................#..#......#........#...#.....#.....##...............#.
                                                  ..............#.........#..#....##...#......#...#.........#...................#..#.#...#........#...
                                                  #.#..#......#............#......#..#..................#...#...#..#.......................#....#.....
                                                  ..............#....#......#....#............##.................#......#...................#.........
                                                  #.......#......#...............#.........#..#.........#..........#.........#.#...............#.#....
                                                  ....##...................#....................#.#................#.#..................##......#.#...
                                                  #.#...#.................#.#.......#....................................#.............#......#.......
                                                  ..#.........#............................#..........##........................#.....................
                                                  ....#....#.#......##..............#............#..#.....#..............##...#...........##..........
                                                  #..#......................#......#.........#...........#...............#............#...........#...
                                                  .......#.....#..#.........#..................#....#...#....................................#.#.#..#.
                                                  ....#....#...........#..........#..........#.....................................#..#............#..
                                                  ....#..#....................#.............##.......#............#.#...#..#...........#.....#........
                                                  ................#........#..........................#......##................#......................
                                                  ..........#.........#........#..........#.............#.......##...........................#........
                                                  .......###.........................#.##................#...#.....#..#..........#......#.............
                                                  ...............................#.....................#....................#.......................#.
                                                  ......#........#...#..............#..........................#......#........#......................
                                                  .............#...........#........................#................................#...........#...#
                                                  .................................#.............#.....#.............#........................#...##..
                                                  ...#......#.#..#..............................#............#................#.......................
                                                  ...............#................#.................##........#........#..............#....#.#........
                                                  ......#.........#.......#...#.........##...#....#.#........#.##.................#......#..#........#
                                                  .#..#........###.............#...#..#............#...#............###...............................
                                                  ...#......................##.......#.................#......#..........#...#....#.......#......#....
                                                  .....#....#...#...........#................#.................................#.............#.#......
                                                  #........#....#.........#..............#....#.....#.#....#.................................#........
                                                  ...##.........#..#..................#...............#.................#..#..........................
                                                  .....#.........#.#...#..#....#..............................#....#..#....#.........#.#.......#...#..
                                                  .#................#........................................................#.............#...#......
                                                  .................................#.......#.....#................###........#.....#......##.#........
                                                  .........##....#..................##..#................#.#....#.#................##..#..............
                                                  .....#.......###..#.................#......#............#.#............#...#...................#....
                                                  ......................#...........................#...#.....................#.#......#............#.
                                                  .................#...#........................#.....#........##.........#.................#....#....
                                                  .......#................#........#.....#...#....#..................#......#...........##.....#......
                                                  ...#..#...........#..............#.#......#.#...........#...#..#.....#........#.....................
                                                  ..#......................................#..#...........#................#..#.#....#..............#.
                                                  ..............#......##.......#........#..#...........#...........................................#.
                                                  ..##.......#....#.#...#........#..................__________________________________________________
                                                  ............#...##........#.#.....#....#...#......__________________________________________________
                                                  ...............#.....#....#...#....#.#.#..........__________________________________________________
                                                  ...##...........................#.............#...__________________________________________________
                                                  .....#..........#......#............#..........##.__________________________________________________
                                                  .............#..................#....#............__________________________________________________
                                                  .#.......................#........................__________________________________________________
                                                  ...#....#..................#......#.............#.__________________________________________________
                                                  ........#..#.....#..........#....#..#.............__________________________________________________
                                                  ...........#.......................#..#...........__________________________________________________
                                                  .....................#.........#........#.........__________________________________________________
                                                  #.........#.#....#...........#......#....##.......__________________________________________________
                                                  ......#...............#........#.........#........__________________________________________________
                                                  ....................................#....#.......#__________________________________________________
                                                  .#............#..............................#...#__________________________________________________
                                                  ..............................##..................__________________________________________________
                                                  ..........#..#....#.....#.............#...........__________________________________________________
                                                  .........#......##..............#........#.#......__________________________________________________
                                                  .........................#............#...........__________________________________________________
                                                  ....#....................#...#....#.........#.....__________________________________________________
                                                  ...#...#.....................#..........#..#.#....__________________________________________________
                                                  ......#.#.......................#.......#...#.....__________________________________________________
                                                  ........................##.................##.....__________________________________________________
                                                  .....#.........#....................#......#......__________________________________________________
                                                  ...#....#..#...#.#....................#..#.....#..__________________________________________________
                                                  ...#..........#.............#.#.................#.__________________________________________________
                                                  ......#....................#................#.....__________________________________________________
                                                  .##....................#...........#.#.....#..#...__________________________________________________
                                                  ........#.........................................__________________________________________________
                                                  ......#.#................#.#...........#..........__________________________________________________
                                                  .....#..#.................................#.#.....__________________________________________________
                                                  #....##.#.........#...........#......#.#..........__________________________________________________
                                                  ..........#.#.......#...........#.................__________________________________________________
                                                  .#......#.#.....#....#......#..................#..__________________________________________________
                                                  ..##..##.......#...........#...........##.........__________________________________________________
                                                  .#...........#....................................__________________________________________________
                                                  #.........#..........#..#.#.........#....#........__________________________________________________
                                                  ....#.....#........#............#.........#....#..__________________________________________________
                                                  ....#......#......#..#.................#..........__________________________________________________
                                                  .#......#.....#......#...........#....#...........__________________________________________________
                                                  ...#.......................#.........#..#...#..#..__________________________________________________
                                                  ....#.......................#.....................__________________________________________________
                                                  ..................#.........##....................__________________________________________________
                                                  ............#...#.......#..........#.#...........#__________________________________________________
                                                  #...............#...#..#....#...#................#__________________________________________________
                                                  ...........#.#..#...##........#..#.........#......__________________________________________________
                                                  ...................#..........#..............#....__________________________________________________
                                                  ..#.#..#...#..#...........#..#............#.......__________________________________________________
                                                  ##.................#......#........#........#.#...__________________________________________________
                                                  ....#......................#...#..#....#.#........__________________________________________________
......#......................#.#...#........#....#......#........#.........#............#........#..__________________________________________________
..#...#..........#...........#...#.#.......................#.....#..#....#.#.#....................#.__________________________________________________
...#................#....#.......#..................#.....#......#...........................#.#....__________________________________________________
...................#..#.....#...............................#...#...#.....................##.......#__________________________________________________
.....#....#...###....................................#.....#....#..........#..#.#..#......#.........__________________________________________________
.##......#..........#..............#...............#............#...................................__________________________________________________
.....##...................#......#........#..#................#................#...................#__________________________________________________
...................#.....#........#..................#..............................................__________________________________________________
...#....#..............#..#............................#..........###...............................__________________________________________________
...........#......#..............................#....#..........................#...........#....#.__________________________________________________
.....#......#..#.#......#............................##....#....##...............#................#.__________________________________________________
...............#........##.....#.........#.#..#..........#..................#....#..#...............__________________________________________________
.........#....#.........#.............#..#.#......#......#.........#..........#.#.##..##....#.##....__________________________________________________
..............................#.#...............................................#.##................__________________________________________________
....................#.........##.....#....#........#..........#..............................#......__________________________________________________
..........#..............#.......#......#.#..#......##.......................#....#....#............__________________________________________________
................#..........#......................................#...#..##.........................__________________________________________________
...................#....#........................................#..#.#..................#..........__________________________________________________
..............#...##...........#.#........#..#.............#............#................#....#.....__________________________________________________
..#.......#............................#.#........#....#...#..............#..#.................#....__________________________________________________
......#................#......#......#..#...............#.......#......##....#.#...#........#.......__________________________________________________
.......#........##................................#.......#......#..................................__________________________________________________
...................#...............##.....#.#......#.#....#...........#...................#.........__________________________________________________
.............#.....#.......................#................#...#...#........####.......#...........__________________________________________________
........###.......##..#..............................#...#.........#........#....#..#....#......#...__________________________________________________
..#...............................#.......#...#.....#..............#....#....##.#...........#.......__________________________________________________
...#........#...#.....#...#.....#...............................#.......#...........................__________________________________________________
.........#...#.......#......#....#..#......##..#......#..............#..........#...........#.......__________________________________________________
.............#........#.#............#.........##..##.#....#..................#.................#..#__________________________________________________
..........#...##...................#.#...#......#.........#................#.....#...............#..__________________________________________________
....#............#......#........................#...#............................................#.__________________________________________________
........###....#.....#..#................................#....#.........#...........#...............__________________________________________________
....#............#..###..#.................................#.....................................#..__________________________________________________
....#.................................................#...#........#.......#.......#.......#........__________________________________________________
..##....#...............#...#............###....#..#.......##.........#.............##..............__________________________________________________
......#......#................#..#...................#..............##......................##......__________________________________________________
#..........#.....................#................#..................#..............................__________________________________________________
.......#...#.......................#..#...........................#..............#..#...........#...__________________________________________________
.#......#....#..........#....#.....#.................#..........#............#......#...............__________________________________________________
...................#.#.#.........................#.................#.......#.........#..............__________________________________________________
#...#.....#..#..............#..#...#...##.........#................#....#..........#..##............__________________________________________________
...............#...#####....................#.......#.#.....#.#.........#.........#..........#......__________________________________________________
..#..#.#.........#..#.........##...#...#..#.##...#............##........................#...........__________________________________________________
............##...#....#...........#.......#............#.......#....#...#......#....................__________________________________________________
.#.#............................##.#.#.....#..........##...#....................##......#..........#__________________________________________________
........#.#...............#.........................#.#.##..............................#.....#.....__________________________________________________
....#...#.........#...................##......#.............................#...#..#......#.........__________________________________________________
#...........#.....#........................#.....#..#........................#.#..........#.........__________________________________________________
..........................#.#........#..#......#.................#.................................#__________________________________________________
.#..##.#.......#.#......#...#..#......#............................................#................__________________________________________________
.....#..........#.......#......#...........#......____________________________________________________________________________________________________
........#.#.#.....#................#.........#....____________________________________________________________________________________________________
......#....#.......#........#............#........____________________________________________________________________________________________________
........#.....#..#..#........................#....____________________________________________________________________________________________________
..............#..............................##..#____________________________________________________________________________________________________
...#....#.#..#............................#.....#.____________________________________________________________________________________________________
.#..........#.....................................____________________________________________________________________________________________________
....#.#.......#.................#................#____________________________________________________________________________________________________
...........#......###.................#...........____________________________________________________________________________________________________
.#.........#..#.............#......#..............____________________________________________________________________________________________________
...............#.#................................____________________________________________________________________________________________________
..#...................#..........#.#.#....#......#____________________________________________________________________________________________________
.#....#.................#.#.......##...#...#...#..____________________________________________________________________________________________________
...#..#.........#...........................#..#..____________________________________________________________________________________________________
#...........#......##...#....#.............#......____________________________________________________________________________________________________
.##.#...........................#...###.......#...____________________________________________________________________________________________________
............................#....................#____________________________________________________________________________________________________
......#...............................#...........____________________________________________________________________________________________________
...........#....................#...#........##.#.____________________________________________________________________________________________________
....#..#.....#.....#............................#.____________________________________________________________________________________________________
..#......#.....#...........#..........#.......#...____________________________________________________________________________________________________
.............#.#...#.......#...#...........#......____________________________________________________________________________________________________
..........#..#.......#........................#...____________________________________________________________________________________________________
............................#..#..................____________________________________________________________________________________________________
............#....#.#.........#.............#......____________________________________________________________________________________________________
...#.....#......#....#.......#.......#............____________________________________________________________________________________________________
.......#.#....................#.....##....#.#.....____________________________________________________________________________________________________
........................#...........##............____________________________________________________________________________________________________
.......#.............................#.....#....#.____________________________________________________________________________________________________
................#..##...#.......#.#...............____________________________________________________________________________________________________
...#........#........................#......#.....____________________________________________________________________________________________________
..........#..........#...................#........____________________________________________________________________________________________________
...............##.......#.................#...#...____________________________________________________________________________________________________
...........#.......#..#......................#....____________________________________________________________________________________________________
....................#..........#.#............#...____________________________________________________________________________________________________
.......#.#......................#.....#...........____________________________________________________________________________________________________
...#..#......#..#........#..#.........#...........____________________________________________________________________________________________________
.#....#...............#.......#.#...#.............____________________________________________________________________________________________________
......................#.........#.........#.....##____________________________________________________________________________________________________
.............#.#.#.#.#...........#.........#......____________________________________________________________________________________________________
...........##...........#...........#..........#.#____________________________________________________________________________________________________
#............................##...#......#......#.____________________________________________________________________________________________________
..........#.....................#.................____________________________________________________________________________________________________
.........#...#........#....#............#........#____________________________________________________________________________________________________
.....#...........#................#...#...#.......____________________________________________________________________________________________________
.#..........#.#.#...#.........#.................#.____________________________________________________________________________________________________
...................#..........#.......##..#......#____________________________________________________________________________________________________
............#......#.........#................#.#.____________________________________________________________________________________________________
..........#...........#..................#.......#____________________________________________________________________________________________________
...................#........#.....................____________________________________________________________________________________________________

36R16L40R15L17L26L39R39R44R36R32L5R46L37R49R29R26L16L29R40R37R42L49R21R23R9R44R32R19R18R10R10R17R46R48R49L10L22L1L5R13R49L5L43R12L23R15R39L12L38L43L39R17L17L46R33L40L35L15L48L34L32R29R35L46R28R19R50L16L33R13R12L47R22R16L10L19L37R21L18R30L13L45R34R49R46L45L2L49L45L36L46L5L43R37L8R46R6L1R45R50L42L31R36L24L43L34R10L37L46R34L15L21L37R19R19R2L44L43R24L34L37L5L20L24L19L40R28R15R15L17L17R45L17R19R45R24L31L41R24R13R36R7L46R27R25R35R6R26R6R6L19R2R16L8L17R14R40L4L17R13R41R12R18R6L2L46R15R46L45R15L29R50L5R50R9R34R25R11L34R7L48L22L1R48L13L14R22R6R43L34L45R4R38R34L47L17R10R48R12L28L8L33L22R47R5L25R18L24L42R43R8L34R5R18R19L39R15L36R37L40L27L22R19L16R12L15L41L18R31R1L26R39R43L30R22R46L13L44R46L40L32L49R47L29R4L42R49L6R4R41L32R15R23L5R29L13R14R17R25R32L6R8R32R21R17R30R17R48L45L35R31R13R45R13R35R33R34R49R2R46R13R40L7L15R21L33L15R29L2R43R25R23R10L45R1L8L10R27L36L39L4L17R46R2L49L12R49R18R41R15L6L44R45L25L15L36L21L4L44L11R5L9R50L48R47L24L32R45R29L39L29L25L22L41R33L46L46R35L38L46L30R45L28L5L48L29R48L35R31L9L42R31R12R26L27R34R14L17L42R29L49L20R6R38L26R38L44L30R17R28L19L4R30R11R33L40R11L46L39R33L38R37L50R7R10L2R3R11L16L40R16L2L9L34L48L45L11R38L46L12R24L47R39L42R19L36R35L30L14R8L19R37R41L2L32L33L47R45R15R11R5L4R28R22R25R42R18L27R27L44R47L12L19L22R41R27R20L6L24L37R49L31L42R21R42L19L6R31L49L39R9R29R22L22L20R29R9R6R46L12L29L21L21L15R21L39L48R9L49L34L1L38L48L23R25L23R5L2L28R3L5L30R36L43L13R38R37R35R10L46R21R34R43R47L5R36L11R25R13L5R33L38R21R18L23L1L42R49R18L23R44L9L8L16L1R1R43R8R36L24R6R20L45R40R31L31R7R48R25L4L22L33L35L37R9R27L23R20L38R43R33L32R1L44R17R15R26L21L33R50L1L13R19L8R48L18R40L32R22R19L22R16R17L20L48L3R28L41R50L23L2R20R1L36R25R40R24R30R33L44R10L8R19L25L38L14R26R34L43L7R16R20R10R40L31R20L44R31L13R2L35L41R6R12L32R2R9L20R36R38L27R15L10R21R26L28R1R26L24L35L5R7L18L33R33R34R30L39R43L14R24L5L37R16L48R22R14R6R9L22L23L35R49R15R4R11L6R34L46R46R48L11L5L42R31R35L26L46L25R30R36R39R48R5R40R28R19R45L42L11R14L32R24R45L46L5R28R33L7L8L23R23L30L22R27L8R47R33L23L21R40L43R30L43R29R34L26L45L26L2R12R45R16R29R16L42L41L42L35R31R24R45R14R5R9R34L6L27L29R17R39R34L45L46R1R26R46R35L48R24R24R31L28L49L48L45L45L37R26L50R49L19R36L8R18L49R22L21L44R49R8L29L5L28R5R50R2L32R17R1R28R31L22L45L18L34R39R36L28R19L16R1L40L11L11R22R4R2L11R30L30L12R36R35R19R20L35L5R1R45R2R31R7R24R37L6L17L48L23L15R1L23L7R19R5R21L22R41R15L32L39L5L31R23R10R20L14R14L23R47L14L39L32L2R13L45R23R49L11R17L13L49R46R45L10L38R17L24L26L20R48R31L23L24R38L47R49L33L29L32L12R23R9L46L36L45R44R28R7R35R39R31R45L16L20R27R37R20R33L32R3R2L35L28R22R4L32R5R39R12R1R2L45R13R24L40R47R40L3R16L34L1R18L11R23R28L3R9L2R49R15R26R12R17R39L14L48L10R9R43L42R3L14L11L25R24R43L22R5L20L6R42R33L35R15L19L34R14R50R32L40R21L16R6R7R46L23R27L27L35L10R3L15L4L15L24L35R44R35R32L34L41R3R26L38R5L50L1L23L16R19R15L28R8R25L4R15L41L15L5R33L33R31L18L39R14R39L10L22L11R11L12R22R14R48L28L25R3L46R27R30R47R44R35R30L29L24L5R24R16R46R49R34R25L27L8L15L4L48R30R40L36L34R35R24L42R49R18L12R7R46L48R45R14R39R29L45L39L15R33R42L42R1R43R38L9L40R50L21R38L32L46L12R49L49R2R17R31L18R8L19R42R50R19L14R50R48L48L22R19R49L2R9L15R24R49L19R38L37R48L29L15L22L32R48L4R26R42R25L7R40R44R42R23L5L32L20L9R22R35R42R45R25L23R29L22L48R1L44R8R7L29R42R24L18R5R30L39R7R31L1L45R2R15R42R38R8R9L17L29L46R2L1L6L47L32L8L36R23L20R13L5L25R39L30R6L26L12L6L12L27R21R30L12R34R17R38R15L30L11R34L48R34R34L13R38L49L21L7R9L22R39L21R25R27L10R45R31R11R38R1L40L39L35L31L25L11L41L24R35R44R11R37R43L41L45L28R25R26R43L11L38L45R39R18L45L46L35L34L41L9L19R34L2L5L17L36R16R28R12L42L18R17R21R1R19R29R47L9L7L31R16R8L37R44R3L44L13R11R9R24L48L3R19R5L5R47L4R22L14L19R45L16L15L20R43R2L25L1R43R15L6L35R1L25L24R11R24R19R46L12L30L16R3L15R23L38R16R14R2R9L39R6L19R1L16L41L23R16L22R45R15R12L5L48L36R38R20L25L33R1L1L22R11R39R22L3R40L40L50R11R32R16L6R1L50L48R21R23L26R34R14R44L38L29L1R4R36L32L14R10R33R50R40R35R11L24L25L27R17L22R26L36L30L42L42L22L44L24L18L50L12R32L50L43R1R43L16L5L2L35L30L11L6L12L29L16R20R31L38L25L19R35R32L36R19R41L19L26L45R50R35L6R38L14L27R31L41L12L12L32R48R6L23R29L17R9L30R12R10R44R11L1R17R8R7R21R36R25R47L44R10R49R37L46L12R11L14R40L42L31L37R18R32R38L22R18R44R43R20L29L6L31L42R27R44R16R29L39R23L25L27L43R37R8L5R24R15L45R36R48L41L43L14R27L8L26R41R46R18R17L15L16R3L10L17L7L12L43R19R22L36L8L21L37R10L5L12L35R31L50L20L4R2R20L6R6L36L46R10R21R14L15R7R18R13R32L17R2L33R19L10R35R8L15L32R20R5R38R21R25L49L16L49R4L50L2L35R43R6R42R4R20R25R40R18L36L12L24R27R19R20R17L27R41L32L10R46L7L7R31R40L6R12R35L43L41R19R43L22R34R24R35L48L45R28L24L10L1L6R48L15L14L29R7L21L30R1L37R40R37L46R41R42R39L45L17R31R12L10R34R30L22L8R35R24R27R25R45R14R14L9L16R25L4L36L29L33L10R13R42L49R40R36L34L48L26L33R12L8R34R13R25L28L42R4R23L1R3L45R4L13R42R27R27R27R41L6L27R2L7L40R10R43R18R33L22R22L16L20R2L34L33R43R16R11L31L3R36L15L1L2R21R2L35R15L7R30R8R37L45R50R35L5R12R28R36L5R7L24L26R12L48L13L33R33R7R35R46L34R30R26R37L23R37R41L44L39L19L13R12L15L33L19R18R26R13L42L26L12L1L36R17L4R5L22R15L49L15R19L3R8L36R20L25R38R36R38R16L3L28R13L1R28R18R29L34R21L45L29R4R49L42R38R42L5L46R8R41L8R2R48L18L27L47L44R3R23L22R33L37L36L38R28L43R43L41L40L19R25R45L20L1R5R33R8R1R42L1L48L30R13L9L4L22L15L2R35R15R20L9L4R47L49R30R31L10R49L49L35L28L19L46R23L50L28L42L25R5R9L7R18R7L2L15R44L28L47R46L23R13L6L34L25L14R41R26R49L32R9R3R10L15R22R42R27R46L12L13R39R15R46L23L31R11L3R45L1L17R49R41R40R14L36R17L43L25R33R50R50R10R24L50L26L25L46R11L28L11R33R39L5R26L14L49R26R13L13R3L46L35L12L48R47R25L38L45R19L27L4L17R50L44R16L10L28R43L16R42R50L20R12R49L27L33R47L23L32L49R24L7L5R49L14L14R20L28L28L14R27L49L43L22R23R17L14L14R24L13L44R44L43L50R31R6R15R39R5R15L40R14L27R43R3R24R1R32L48R29R38L31R16R18L12L1L31L1R7L17R25L15L28R46R39R26L15L20R2R45L46L41R32L22R16L30R50R50R46L50R47L16R47L40L40L5L23L47R14L20R14L19R50L1L1L23R19L43R25R20L32R38L10R40L30L25L16L43R14L44R49R4L31R37L35R41R40R14L30R41L42'''

data = data.replace("_", " ")
# data = data_test

data = data.split('\n')
path = data[-1]
data = data[:-2]
# print(path, data)
# for row in data: print(row)
# print(data[5][3])


chars = '>v<^'
def print_board(board, pos, dir):
  old = board[pos[0]][pos[1]]
  board[pos[0]][pos[1]] = chars[dir]
  for row in board:
    print(''.join(row))
  print()
  board[pos[0]][pos[1]] = old

# data = [row.strip() for row in data]
data = [[c for c in row] for row in data if row]
# data = list(map(int, data))
# data = [row.split() for row in data]

dirs = [
  (0, 1), # right
  (1, 0), # bottom
  (0, -1),
  (-1, 0),
]

path = re.findall("\d+[R|L]", path)
path = [(int(c[:-1]), c[-1]) for c in path]

def move(data, path):
  start = (0, 0)
  while data[start[0]][start[1]] == ' ':
    start = (start[0], start[1] + 1)
  # print(start, data[start[0]][start[1]])
  dir = 0

  pos = start
  n = len(data)
  m = len(data[0])

  for (steps, turn) in path:
    forward = dirs[dir]
    # print_board(data, pos, dir)
    for i in range(steps):
      new_pos = (pos[0] + forward[0]) % n, (pos[1] + forward[1]) % m
      # print(i, dir, dirs[dir], pos, new_pos)
      # print(new_pos, n, m)
      # print(new_pos, data[new_pos[0]], len(data[new_pos[0]]))
      while data[new_pos[0]][new_pos[1]] == ' ':
        # wrap around
        # print(new_pos, n, m)
        new_pos = (new_pos[0] + forward[0]) % n, (new_pos[1] + forward[1]) % m

      if data[new_pos[0]][new_pos[1]] == '#':
        # it's a wall
        continue
      else:
        pos = new_pos
    if turn == 'R':
      dir = (dir + 1) % len(dirs)
    elif turn == 'L':
      dir = (dir - 1 + len(dirs)) % len(dirs)
    # print(steps, turn)
  # print_board(data, pos, dir)
  print(pos, dir)
  return 1000 * (pos[0] + 1) + (pos[1] + 1) * 4 + dir

print(move(data, path))
exit()
# 6032

# pprint.pprint(data)
result = 0



print(result)

print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
