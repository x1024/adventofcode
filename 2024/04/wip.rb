input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

def parse_input(input)
  input.split("\n").map.with_index do |line, x|
    line.each_char.map.with_index { |c, y| [x + y.i, c] }
  end.flatten(1).to_h
end

def main(input, paths, str)
  data = parse_input(input)
  data.keys.sum do |pos|
    paths.filter { |path| data.values_at(*path.map { pos + _1 }) == str }.count
  end
end

paths1 = [
  [0, 0 + 1i, 0 + 2i, 0 + 3i],
  [0, 1, 2, 3],
  [0, 1 + 1i, 2 + 2i, 3 + 3i],
  [0, -1 + 1i, -2 + 2i, -3 + 3i]
]
paths1 += paths1.map { |p| p.map { |x| x * 1i } }
str1 = %w[X M A S]

paths2 = [
  [0, 1 + 1i, 2 + 2i, 2, 0 + 2i],
  [0, 1 + 1i, 2 + 2i, 0 + 2i, 2],
  [2 + 2i, 1 + 1i, 0, 0 + 2i, 2],
  [2 + 2i, 1 + 1i, 0, 2, 0 + 2i]
]
str2 = %w[M A S M S]

p main(input_sample, paths1, str1)
p main(input_real, paths1, str1)

p main(input_sample, paths2, str2)
p main(input_real, paths2, str2)
