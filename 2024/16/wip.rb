require 'pqueue'

input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

def main(input)
  data = input.split("\n").map.with_index do |line, x|
    line.each_char.map.with_index { |c, y| [x + y.i, c] }
  end.flatten(1).to_h

  start = data.keys.filter { |k| data[k] == 'S' }.first
  finish = data.keys.filter { |k| data[k] == 'E' }.first
  offsets = [1, 1i, -1, -1i]

  seen = {}
  prev = {}

  q = PQueue.new([[start, 1i, 0, nil]]) { |a, b| a[2] > b[2] }
  while ((pos, dir, score) = q.shift)
    key = [pos, dir].hash
    next if seen.fetch(key, score + 1) <= score

    seen[key] = score
    next if pos == finish

    offsets.each do |offset|
      next_pos = pos + offset
      next unless data.key? next_pos
      next if data[next_pos] == '#' || dir == -offset

      next_pos = pos + offset
      next_score = score + (dir == offset ? 1 : 1001)
      q << [next_pos, offset, next_score]
      (prev[[next_pos, offset, next_score].hash] ||= []) << [pos, dir, score]
    end
  end

  result = offsets.map { seen.fetch([finish, _1].hash, 1 << 31) }.min
  q = offsets.map { [finish, _1, result] }
  all = Set.new
  while ((pos,) = key = q.shift)
    all << pos
    q += prev.delete(key.hash) || []
  end

  [result, all.size]
end

p main(input_sample)
p main(input_real)
