input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:
=begin
You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.
=end

def check(data, pos)
  # pos = data.find { |_, c| c == '^' }[0]
  # p pos
  # data[pos] = '.'
  def key(pos, dir) = "#{pos.real},#{pos.imag},#{dir}"
  seen = {}
  dir = -1
  steps = 0
  while true
    if data[pos + dir].nil?
      return 0
    elsif data[pos + dir] == '.'
      a = key(pos, dir)
      return 1 if seen[a]

      seen[a] = true

      pos += dir
      steps += 1
    else
      dir *= 1.i * 1.i * 1.i
    end
  end
  true
end

def main(input)
  lines = input.split("\n")

  data = lines.map do |line|
    line.scan(/\d+/)
  end

  # convert data to a hash with complex coordinates
  data = input.split("\n").map.with_index do |line, x|
    line.each_char.map.with_index { |c, y| [x + y.i, c] }
  end.flatten(1).to_h

  p1 = data.find { |_, c| c == '^' }[0]
  data[p1] = '.'

  result = data.keys.map do |pos|
    old = data[pos]
    data[pos] = '#'
    res = check data, p1
    data[pos] = old
    p [pos, res]
    res
  end.sum

  # p lines
  # p data

  puts 'Result:', result
end

result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
