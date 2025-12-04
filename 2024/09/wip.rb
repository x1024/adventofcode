require 'rb_heap'

input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

def main(input)
  holes = Hash.new { |h, k| h[k] = Heap.new }
  files = []
  index = 0
  input.ljust(input.size + input.size % 2, '0').each_char.map(&:to_i)
       .each_slice(2).with_index do |(file, hole), i|
    files << [i, file, index]
    index += file
    holes[hole] << index
    index += hole
  end

  find_hole = lambda do |length, min_pos|
    (length..9)
      .filter {|k| !holes[k].empty? && holes[k].peak < min_pos }
      .min { |a, b| holes[a].peak <=> holes[b].peak }
  end

  files.reverse.sum do |id, length, pos|
    if (hole = find_hole.(length, pos))
      (pos = holes[hole].pop)
      holes[hole - length] << pos + length
    end
    id * (length * (length - 1) / 2 + pos * length)
  end
end

p main(input_sample)
p main(input_real)
