input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

def debug(data)
  # print the grid
  print ((0..data.keys.map { |k| k.imag }.max).map do |x|
    (0..data.keys.map { |k| k.real }.max).map do |y|
      data[x + y.i]
    end.join
  end).join("\n") + "\n"
end

def key(pos, dir) = "#{pos.real},#{pos.imag},#{dir}"

def check(data, pos, new_obstacle = nil)
  data = data.dup
  data[new_obstacle] = '#' if new_obstacle
  dir = -1
  seen = Set.new
  seen2 = Set.new
  while true
    new_pos = pos + dir
    seen.add(pos)
    if data[new_pos].nil?
      return seen
    elsif data[new_pos] != '#'
      k = key(pos, dir)
      return -1 if seen2.include? k

      seen.add(pos)
      seen2.add(k)
      pos = new_pos
    else
      dir *= 1.i * 1.i * 1.i
    end
  end
  true
end

def main(input)
  data = input.split("\n").map.with_index do |line, x|
    line.each_char.map.with_index { |c, y| [x + y.i, c] }
  end.flatten(1).to_h

  start = data.find { |_, c| c == '^' }[0]
  data[start] = '.'

  path = check data, start
  p path.size
  path.filter.with_index do |new_obstacle, i|
    p [i, new_obstacle]
    check(data, start, new_obstacle) == -1
  end.size

  # p lines
  # p data
end

result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
