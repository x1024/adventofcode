input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:
=begin
You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).
=end

def check(line)
  result, *numbers = line[0].to_i, *line[1..-1].map(&:to_i)
  0.upto(2**numbers.size - 1) do |mask|
    sum = numbers[0]
    (1...numbers.size).each do |i|
      num = numbers[i]
      if mask[i - 1] == 0
        sum += num
      else
        sum *= num
      end
    end
    return result if sum == result
  end
  0
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

  result = data.sum { |d| check d }

  # p lines
  # p data

  puts 'Result:', result
end

result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
