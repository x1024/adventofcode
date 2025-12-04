input = File.read 'input-sample.txt', encoding: 'utf-8'
input = File.read 'input.txt', encoding: 'utf-8'

data = input.split("\n").map.with_index do |line, x|
  line.each_char.map.with_index { |c, y| [x + y.i, c.to_i] }
end.flatten(1).to_h

offsets = [1, -1, 1.i, -1.i]
result = data.sum do |pos, val|
  next 0 unless val == 0

  paths = Hash.new 0
  queue = [pos]

  while (current = queue.shift)
    paths[current] += 1
    queue += offsets.map { |o| current + o }.filter { |p| data[p] == data[current] + 1 }
  end

  data.filter { |_, v| v == 9}.sum { |k, _| (paths[k] > 0 ? 1 : 0) + paths[k].i }
end
p result.real, result.imag
