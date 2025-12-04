input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:
#
#    As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.
#
# This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:
#
#
# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....
# The actual word search will be full of letters instead. For example:
#
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:
#
# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX
# Take a look at the little Elf's word search. How many times does XMAS appear?
#    The Elf looks quizzically at you. Did you misunderstand the assignment?
#
# Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:
#
# M.S
# .A.
# M.S

def check(line)
  true
end

def main(input)
  data = input.split("\n")
  p1 = [
    [
      [0, 0], [0, 1], [0, 2], [0, 3]
    ],
    [
      [0, 0], [1, 0], [2, 0], [3, 0]
    ],
    [
      [0, 0], [1, 1], [2, 2], [3, 3]
    ],
    [
      [0, 0], [1, -1], [2, -2], [3, -3]
    ]
  ]
  p2 = [
    [
      [0, 0], [1, 1], [2, 2], [0, 2], [2, 0]
    ],
    [
      [0, 0], [1, 1], [2, 2], [2, 0], [0, 2]
    ],
    [
      [2, 2], [1, 1], [0, 0], [0, 2], [2, 0]
    ],
    [
      [2, 2], [1, 1], [0, 0], [2, 0], [0, 2]
    ]
  ]
  paths = p2
  # paths += p1.map { |p| p.map { |x, y| [x, y] } }
  # paths += p1.map { |p| p.map { |x, y| [-x, -y] } }
  # paths += p2.map { |p| p.map { |x, y| [x, y] } }
  # paths += p2.map { |p| p.map { |x, y| [-x, -y] } }

  # pp paths
  # pp paths.count
  # str = %w[X M A S]
  str = %w[M A S M S]
  result = 0
  (0..data.size - 1).each do |i|
    (0..data[i].size - 1).each do |j|
      found = false
      paths.each do |path|
        found = path.zip(str).filter do |pos, c|
          x = pos[0] + i
          y = pos[1] + j
          if x < 0 || y < 0 || x >= data.size || y >= data[i].size
            false
          else
            data[x][y] == c
          end
        end.size == str.size
        # p "Found: #{found} at #{i}, #{j}" if found
        result += 1 if found
      end
    end
  end

  puts 'Result:', result
  result
end

result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
