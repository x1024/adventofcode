ADJANCENT = [-1 + -1.i, -1.i, 1 + -1.i, -1, 1, -1 + 1.i, 1.i, 1 + 1.i]

grid = {}

File.read('input-rb.txt').lines.each_with_index do |line, y|
  line.chomp.chars.each_with_index do |char, x|
    grid[x + y.i] = char
  end
end

def number(grid, pos)
  return nil unless grid.fetch(pos, '') =~ /\d/
  left, right = pos, pos
  left -= 1 while grid.fetch(left - 1, '') =~ /\d/
  right += 1 while grid.fetch(right + 1, '') =~ /\d/
  [(left.real..right.real).map { grid[_1.real + pos.imag.i] }.join.to_i, left, right]
end

symbols = grid.filter { _2 !~ /[.\d]/ }.map { |p, char| [char, ADJANCENT.map { number grid, _1 + p }.compact.uniq] }

p symbols.flat_map { _2 }.uniq.sum(&:first)
p symbols.filter { |char, nums| char == ?* && nums.size == 2 }.sum { |_, nums| nums.map(&:first).reduce(:*) }
