input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:
#    The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!
#
# It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.
#
# However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.
#
# For example, consider the following section of corrupted memory:
#
# xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
# Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).
#
# Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?
#
#    There are two new instructions you'll need to handle:
#
# The do() instruction enables future mul instructions.
# The don't() instruction disables future mul instructions.
# Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.
#
# For example:
#
# xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
# This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.
#

def check(line)
  p line
  true
end

def main(input)
  lines = input.split("\n")
  result = 0
  enabled = true
  input.scan(/mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))/) do |match|
    if match[2]
      enabled = true
    elsif match[3]
      enabled = false
    elsif enabled
      p match
      result += match[0].to_i * match[1].to_i
    end
  end
  p input
  p result

  # result = data.map check

  # p lines
  # p data

  puts 'Result:', result
end

input_sample = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
