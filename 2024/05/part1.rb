input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:

def check(line)
  p line
  true
end

def main(input)
  rules, pages = input.split("\n\n")

  rules = rules.split("\n").map do |line|
    line.scan(/\d+/).map(&:to_i)
  end
  pages = pages.split("\n").map do |line|
    line.scan(/\d+/).map(&:to_i)
  end

  result = pages.filter! do |page|
    rules.all? do |rule|
      ia = page.index(rule[0])
      ib = page.index(rule[1])
      p "#{page} #{rule} #{ia} < #{ib}"
      !ia || !ib || ia < ib
    end
  end.sum do |page|
    p 'asd', page
    page[(page.count - 1) / 2]
  end

  puts 'Result:', result
  result
end

result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
