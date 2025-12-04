def bfs(data, start)
  q = [start]
  visited = { start => 0 }
  offsets = [1, -1, 1.i, -1.i]
  while (current = q.shift)
    offsets.each do |offset|
      new = current + offset
      next if data[new] == '#' || visited.key?(new)

      visited[new] = visited[current] + 1
      q << new
    end
  end
  Hash.new(0).merge visited
end

def solve(input, dist = 20, limit = 100)
  grid = input.lines.flat_map.with_index { |line, x| line.chars.map.with_index { |c, y| [x + y.i, c] } }.to_h
  dists = bfs(grid, grid.filter { _2 == 'S' }.first.first)
  range = (-dist..dist).to_a
  neighbors = range.product(range).map { [_1 + _2.i, _1.abs + _2.abs] }.select { _2 <= dist }
  dists.sum { |p, d| neighbors.map { dists[p + _1] - _2 }.count { _1 - d >= limit } }
end

input = File.read 'input.txt', encoding: 'utf-8'
p solve(input, 2, 100)
p solve(input, 20, 100)
