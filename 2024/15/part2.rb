input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'
DEBUG = false

# Task description:
=begin
--- Day 15: Warehouse Woes ---

You appear back inside your own mini submarine! Each Historian drives their mini submarine in a different direction; maybe the Chief has his own submarine down here somewhere as well?

You look up to see a vast school of lanternfish swimming past you. On closer inspection, they seem quite anxious, so you drive your mini submarine over to see if you can help.

Because lanternfish populations grow rapidly, they need a lot of food, and that food needs to be stored somewhere. That's why these lanternfish have built elaborate warehouse complexes operated by robots!

These lanternfish seem so anxious because they have lost control of the robot that operates one of their most important warehouses! It is currently running amok, pushing around boxes in the warehouse with no regard for lanternfish logistics or lanternfish inventory management strategies.

Right now, none of the lanternfish are brave enough to swim up to an unpredictable robot so they could shut it off. However, if you could anticipate the robot's movements, maybe they could find a safe option.

The lanternfish already have a map of the warehouse and a list of movements the robot will attempt to make (your puzzle input). The problem is that the movements will sometimes fail as boxes are shifted around, making the actual movements of the robot difficult to predict.

For example:

##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^

As the robot (@) attempts to move, if there are any boxes (O) in the way, the robot will also attempt to push those boxes. However, if this action would cause the robot or a box to move into a wall (#), nothing moves instead, including the robot. The initial positions of these are shown on the map at the top of the document the lanternfish gave you.

The rest of the document describes the moves (^ for up, v for down, < for left, > for right) that the robot will attempt to make, in order. (The moves form a single giant sequence; they are broken into multiple lines just to make copy-pasting easier. Newlines within the move sequence should be ignored.)

Here is a smaller example to get started:

########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<

Were the robot to attempt the given sequence of moves, it would push around the boxes as follows:

Initial state:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move <:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#..@OO.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.@...#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#..@O..#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#...@O.#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#....@O#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#.....O#
#.#.O@.#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

The larger example has many more moves; after the robot has finished those moves, the warehouse would look like this:

##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########

The lanternfish use their own custom Goods Positioning System (GPS for short) to track the locations of the boxes. The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map plus its distance from the left edge of the map. (This process does not stop at wall tiles; measure all the way to the edges of the map.)

So, the box shown below has a distance of 1 from the top edge of the map and 4 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 4 = 104.

#######
#...O..
#......

The lanternfish would like to know the sum of all boxes' GPS coordinates after the robot finishes moving. In the larger example, the sum of all boxes' GPS coordinates is 10092. In the smaller example, the sum is 2028.

Predict the motion of the robot and boxes in the warehouse. After the robot is finished moving, what is the sum of all boxes' GPS coordinates?
=end

def transform(data)
  data2 = {}
  data.keys.map do |k|
    p1 = k.real + k.imaginary * 2.i
    p2 = k.real + k.imaginary * 2.i + 1.i
    # p [k, p1, p2]
    case data[k]
    when '#'
      data2[p1] = '#'
      data2[p2] = '#'
    when 'O'
      data2[p1] = '['
      data2[p2] = ']'
    when '@'
      data2[p1] = '@'
      data2[p2] = '.'
    when '.'
      data2[p1] = '.'
      data2[p2] = '.'
    end
  end
  # pr(data2)
  data2
end

def pr(data)
  mx = data.keys.max_by(&:real).real
  my = data.keys.max_by(&:imaginary).imaginary
  0.upto(mx) do |x|
    p 0.upto(my).map { |y| data[x + y.i] }.join
  end
end

def checksum(data)
  data.keys.filter { |k| 'O['.include? data[k] }.map { |k| k.real * 100 + k.imaginary }.sum
end

def try_move(data, pos, move, movers)
  actor = data[pos]
  return false if actor == '#'
  return true if actor == '.'
  return try_move(data, pos - 1.i, move, movers) if actor == ']' && '^v'.include?(move)

  offset = 0
  case move
  when '<'
    offset = - 1.i
  when '>'
    offset = + 1.i
  when '^'
    offset = - 1
  when 'v'
    offset = + 1
  end
  new_pos = pos + offset
  can_move = if '^v'.include?(move) && actor == '['
               try_move(data, new_pos, move, movers) &&
                 try_move(data, new_pos + 1.i, move, movers)
             else
               try_move(data, new_pos, move, movers)
             end
  if can_move
    movers << [pos, new_pos]
    movers << [pos + 1.i, new_pos + 1.i] if '^v'.include?(move) && actor == '['
  end

  can_move
end

def main(input, do_transform: true)
  map, moves = input.split("\n\n")
  moves = moves.split.join.chars

  # convert data to a hash with complex coordinates
  data = map.split("\n").map.with_index do |line, x|
    line.each_char.map.with_index { |c, y| [x + y.i, c] }
  end.flatten(1).to_h
  # data[robot] = '.' # remove robot from the map
  data = transform(data) if do_transform

  # pr(data)
  moves.each.with_index do |move, i|
    data.keys.filter { |k| data[k] == '[' }.each do |k|
      # p [i, moves.size, move]
      throw 'adasdasd' if data[k + 1.i] != ']'
    end
    robot = data.keys.find { |k| data[k] == '@' } # find robot
    # p robot
    movers = []
    can_move = try_move(data, robot, move, movers)
    if can_move
      data2 = data.dup
      movers.each do |mover|
        data2[mover[0]] = '.'
      end
      movers.each do |mover|
        data2[mover[1]] = data[mover[0]]
      end
      data = data2
    end
    p [i, moves.size, move, can_move]
    if DEBUG
      p [i, moves.size, move, can_move]
      p '---'
      pr data
      p [i, moves.size, move, moves[i+1], can_move]
      gets
    end
  end

  checksum(data)
end

input_sample2 = <<~DATA
  ########
  #..O.O.#
  ##@.O..#
  #...O..#
  #.#.O..#
  #...O..#
  #......#
  ########

  <^^>>>vv<v>>v<<
DATA

input_sample3 = <<~DATA
  #######
  #...#.#
  #.....#
  #..OO@#
  #..O..#
  #.....#
  #######

  <vv<<^^<<^^
DATA

input_sample4 = <<~DATA
  #######
  #...#.#
  #..#..#
  #..OO.#
  #..@..#
  #.....#
  #######

  <^>v>^>^>^
DATA
# result = main(input_sample4)
# p result
result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
