MOD = 131
STEPS = 26501365

grid = File.read('input.txt').lines.flat_map.with_index { |l, y| l.chomp.chars.map.with_index { [_2 + y.i, _1] } }.to_h

def reachable(grid, steps)
  reached, left = {}, [[grid.detect { _2 == ?S }.first, 0]]

  while left.shift in pos, count
    next if grid[pos.real % MOD + pos.imag % MOD * 1i] == '#' || reached[pos] || count > steps
    reached[pos] = count if count % 2 == steps % 2
    [1, -1, 1i, -1i].each { left << [pos + _1, count + 1] }
  end

  reached
end

def count(reached, x, y) = (0..130).to_a.product((0..130).to_a).count { reached[x * 131 + _1 + (y * 131 + _2).i] }

p reachable(grid, 64).size

steps = STEPS / MOD
reached = reachable(grid, MOD * 2 + MOD / 2)

p count(reached, 1, 0) * (steps ** 2) +
  count(reached, 0, 0) * (steps.pred ** 2) +
  [[-2, 0], [2, 0], [0, 2], [0, -2]].sum { count(reached, *_1) } +
  [[-1, -2], [-1, 2], [1, -2], [1, 2]].sum { count(reached, *_1) * steps } +
  [[1, 1], [1, -1], [-1, 1], [-1, -1]].sum { count(reached, *_1) * steps.pred }
