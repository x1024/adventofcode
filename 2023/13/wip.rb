def diff(a, b) = a.zip(b).count { _1 != _2 }
def fold(lines, i) = lines[...i].reverse.zip(lines.drop(i)).filter { _2 }
def find(lines, target) = 1.upto(lines.size - 1).detect { |i| target == fold(lines, i).sum { diff(*_1) } } || 0
def score(grid, target) = find(grid, target) * 100 + find(grid.transpose, target)

grids = File.read('input.txt').split("\n\n").map { |chunk| chunk.lines.map { _1.chomp.chars } }
p grids[0]

1i.rect.each { |t| p grids.sum { score(_1, t) } }
