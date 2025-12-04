input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:
=begin
--- Day 18: RAM Run ---

You and The Historians look a lot more pixelated than you remember. You're inside a computer at the North Pole!

Just as you're about to check out your surroundings, a program runs up to you. "This region of memory isn't safe! The User misunderstood what a pushdown automaton is and their algorithm is pushing whole bytes down on top of us! Run!"

The algorithm is fast - it's going to cause a byte to fall into your memory space once every nanosecond! Fortunately, you're faster, and by quickly scanning the algorithm, you create a list of which bytes will fall (your puzzle input) in the order they'll land in your memory space.

Your memory space is a two-dimensional grid with coordinates that range from 0 to 70 both horizontally and vertically. However, for the sake of example, suppose you're on a smaller grid with coordinates that range from 0 to 6 and the following list of incoming byte positions:

5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0

Each byte position is given as an X,Y coordinate, where X is the distance from the left edge of your memory space and Y is the distance from the top edge of your memory space.

You and The Historians are currently in the top left corner of the memory space (at 0,0) and need to reach the exit in the bottom right corner (at 70,70 in your memory space, but at 6,6 in this example). You'll need to simulate the falling bytes to plan out where it will be safe to run; for now, simulate just the first few bytes falling into your memory space.

As bytes fall into your memory space, they make that coordinate corrupted. Corrupted memory coordinates cannot be entered by you or The Historians, so you'll need to plan your route carefully. You also cannot leave the boundaries of the memory space; your only hope is to reach the exit.

In the above example, if you were to draw the memory space after the first 12 bytes have fallen (using . for safe and # for corrupted), it would look like this:

...#...
..#..#.
....#..
...#..#
..#..#.
.#..#..
#.#....

You can take steps up, down, left, or right. After just 12 bytes have corrupted locations in your memory space, the shortest path from the top left corner to the exit would take 22 steps. Here (marked with O) is one such path:

OO.#OOO
.O#OO#O
.OOO#OO
...#OO#
..#OO#.
.#.O#..
#.#OOOO

Simulate the first kilobyte (1024 bytes) falling onto your memory space. Afterward, what is the minimum number of steps needed to reach the exit?
=end

def check(line)
  p line
  true
end

def pr(data)
  mx = data.keys.max_by(&:real).real
  my = data.keys.max_by(&:imaginary).imaginary
  p [mx, my]
  0.upto(mx).map do |x|
    p 0.upto(my).map { |y| data[x + y.i] }.join
  end
end

def bfs(data, start, finish)
  q = [start]
  visited = { start => 0 }
  offsets = [1, -1, 1.i, -1.i]
  data[start] = 0
  while (now = q.shift)
    if now == finish
      # p 'done'
      # pr(data)
      # pp visited
      # p finish
      return visited[now]
    end
    next if now.real < 0 || now.imag < 0
    next if now.real > finish.real || now.imag > finish.imag

    offsets.each do |offset|
      next_pos = now + offset
      next if data[next_pos] == '#' || visited[next_pos]
      next if data[next_pos] != '.'

      visited[next_pos] = visited[now] + 1
      data[next_pos] = visited[next_pos] % 10
      q << next_pos
    end
  end
end

def sim(lines, finish, limit)
  data = Hash.new('.')
  lines[0...limit].map do |coords|
    data[coords] = '#'
  end
  # pr data

  bfs(data, 0 + 0.i, finish)
end

def main(input, finish, limit)
  lines = input.split("\n").map do |line|
    coords = line.scan(/\d+/).map(&:to_i)
    coords[0] + coords[1].i
  end
  res_a = sim(lines, finish, limit)
  p res_a

  while true
    limit += 1
    r = sim(lines, finish, limit)
    p [limit, lines[limit-1], r]
    return lines[limit-1] if r.nil?
  end
end

# result = main(input_sample, 6 + 6.i, 12)
# p result
result = main(input_real, 70 + 70.i, 1024)
p result
require 'clipboard'
Clipboard.copy result
