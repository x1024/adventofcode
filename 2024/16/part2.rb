input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:
=begin
--- Day 16: Reindeer Maze ---

It's time again for the Reindeer Olympics! This year, the big event is the Reindeer Maze, where the Reindeer compete for the lowest score.

You and The Historians arrive to search for the Chief right as the event is about to start. It wouldn't hurt to watch a little, right?

The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E). They can move forward one tile at a time (increasing their score by 1 point), but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000 points).

To figure out the best place to sit, you start by grabbing a map (your puzzle input) from a nearby kiosk. For example:

###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############

There are many paths through this maze, but taking any of the best paths would incur a score of only 7036. This can be achieved by taking a total of 36 steps forward and turning 90 degrees a total of 7 times:

###############
#.......#....E#
#.#.###.#.###^#
#.....#.#...#^#
#.###.#####.#^#
#.#.#.......#^#
#.#.#####.###^#
#..>>>>>>>>v#^#
###^#.#####v#^#
#>>^#.....#v#^#
#^#.#.###.#v#^#
#^....#...#v#^#
#^###.#.#.#v#^#
#S..#.....#>>^#
###############

Here's a second example:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################

In this maze, the best paths cost 11048 points; following one such path would look like this:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################

Note that the path shown above includes one 90 degree turn as the very first move, rotating the Reindeer from facing East to facing North.

Analyze your map carefully. What is the lowest score a Reindeer could possibly get?0
=end

def check(line)
  p line
  true
end

def pr(data)
  mx = data.keys.max_by(&:real).real
  my = data.keys.max_by(&:imaginary).imaginary
  0.upto(mx) do |x|
    p 0.upto(my).map { |y| data[x + y.i] }.join
  end
end

def main(input)
  lines = input.split("\n")

  data = input.split("\n").map.with_index do |line, x|
    line.each_char.map.with_index { |c, y| [x + y.i, c] }
  end.flatten(1).to_h
  pr data

  start = data.keys.filter { |k| data[k] == 'S' }.first
  finish = data.keys.filter { |k| data[k] == 'E' }.first
  p start, finish
  # p lines
  # p data
  offsets = [1, 1i, -1, -1i]
  q = [
    [start, 1i, 0, []]
  ]
  result = 1000 * 1000 * 1000
  seen = {}
  ends = []
  paths = []
  while q.any?
    pos, dir, score, path = q.shift
    key = [pos, dir].hash
    if seen.key? key
      s = seen[key][:score]
      if s < score
        next
      elsif s > score
        seen[key] = { score:, path: }
      else
        seen[key][:path] << path
      end
    else
      seen[key] = { score:, path: }
    end

    if pos == finish
      if score < result
        result = score
        paths = [path]
      elsif score == result
        paths << path
      end
      # result = [result, score].min
      # ends << [pos, dir].hash
      next
    end
    offsets.each do |offset|
      next_pos = pos + offset
      next unless data.key? next_pos
      next if data[next_pos] == '#'

      next if dir == -offset

      next_pos = pos + offset
      next_score = score + (dir == offset ? 1 : 1001)
      next_path = path.dup << pos
      q << [next_pos, offset, next_score, next_path]
    end
  end

  p result
  p paths.flatten.uniq.size + 1
  exit

  seen2 = Set.new
  q2 = ends.map { [finish, _1] }
  while q2.any?
    pos, dir = q2.shift
    key = [pos, dir].hash
    data = seen[key]
    p [pos, dir]
    exit
  end

  offsets.each do |offset|
    key = [finish, offset].hash
    p seen[key]
  end

  result
end

input_sample = <<~DATA
  #################
  #...#...#...#..E#
  #.#.#.#.#.#.#.#.#
  #.#.#.#...#...#.#
  #.#.#.#.###.#.#.#
  #...#.#.#.....#.#
  #.#.#.#.#.#####.#
  #.#...#.#.#.....#
  #.#.#####.#.###.#
  #.#.#.......#...#
  #.#.###.#####.###
  #.#.#...#.....#.#
  #.#.#.#####.###.#
  #.#.#.........#.#
  #.#.#.#########.#
  #S#.............#
  #################
DATA
# result = main(input_sample)
# p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
