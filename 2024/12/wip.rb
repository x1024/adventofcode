NEIGHBORS = [1, -1, 1i, -1i].freeze

def dfs(start, data, visited)
  val = data[start]
  stack = [start]
  res = Set.new
  while (pos = stack.pop)
    next if data[pos] != val || visited.include?(pos)

    visited << pos
    res << pos
    stack.concat(NEIGHBORS.map { |n| pos + n })
  end

  res
end

data = File.read('input.txt', encoding: 'utf-8')
           .split("\n").map.with_index do |line, x|
  line.each_char.map.with_index { |c, y| [x + y.i, c] }
end.flatten(1).to_h
visited = Set.new
regions = data.keys.map { |key| dfs(key, data, visited) }
p(regions.sum { |r| r.size * r.sum { |p| NEIGHBORS.count { |n| !r.include?(p + n) } } })
p(regions.sum do |r|
  r.size * r.sum do |p|
    NEIGHBORS.count do |n|
      !r.include?(p + n) && !((r.include? p + n*1.i) && !r.include?(p + n*1.i + n))
    end
  end
end)
