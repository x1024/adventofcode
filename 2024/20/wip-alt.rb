def bfs(data, start)
  q = [[start, 0]]
  visited = { start => 0 }
  offsets = [1, -1, 1.i, -1.i]
  while q.any?
    current, distance = q.shift
    next if visited[current] < distance

    offsets.each do |offset|
      new = current + offset
      next if visited[new] || data[new] == '#'

      visited[new] = distance + 1
      q << [new, distance + 1]
    end
  end
  Hash.new(0).merge visited
end

def main(input, dist = 20, limit = 100)
  data = input.split("\n").map.with_index do |line, x|
    line.each_char.map.with_index { |c, y| [x + y.i, c] }
  end.flatten(1).to_h

  distances = bfs(data, data.keys.filter { data[_1] == 'S' }.first)
  path = distances.sort_by(&:last).map(&:first)

  (0...path.count).sum do |i|
    p1 = path[i]
    (i+1...path.count).count do |i2|
      p2 = path[i2]
      d = p2 - p1
      d = d.real.abs + d.imag.abs
      d <= dist && i2 - i - d >= limit
    end
  end
end

input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

p main(input_sample, 2, 2)
p main(input_sample, 20, 2)
p main(input_real, 2, 100)
p main(input_real, 20, 100)
