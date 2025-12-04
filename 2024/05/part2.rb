input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:

def check(line)
  p line
  true
end

def main(input)
  rules_def, pages = input.split("\n\n")

  rules = {}
  rules_def.split("\n").map do |line|
    a, b = line.scan(/\d+/).map(&:to_i)
    rules[a] ||= []
    rules[a] << b
  end

  pages = pages.split("\n").map do |line|
    line.scan(/\d+/).map(&:to_i)
  end

  result = pages.map do |page|
    page_correct = page.dup
    page.each do |a|
      r = (rules[a] || []).filter { |b| page.include?(b) }

      [r.count, a]
      page_correct[r.count] = a
    end
    page_correct = page_correct.reverse
    res = page.map.with_index.any? { |a, i| a != page_correct[i] }
    p [page, page_correct, res]
    [res, page_correct]
  end.filter { |res, _| res }.map { |_, page| page }
                .sum { |page| page[(page.count - 1) / 2] }

  puts 'Result:', result
  result
end

result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
