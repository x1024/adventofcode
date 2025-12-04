input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:
=begin
=end

def check(line)
  p line
  true
end

def main(input)
  lines = input.split("\n")

  data = lines.map do |line|
    line.scan(/\d+/)
  end

  # convert data to a hash with complex coordinates
  # data = input.split("\n").map.with_index do |line, x|
  #   line.each_char.map.with_index { |c, y| [x + y.i, c] }
  # end.flatten(1).to_h

  result = data.map { |d| check d }

  # p lines
  # p data

  p result
  result
end

result = main(input_sample)
p result
result = main(input_real)
# p result
require 'clipboard'
Clipboard.copy result
