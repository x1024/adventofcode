input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

def main(input)
  l = input.split("\n").map { _1.scan(/\d+/).map(&:to_i) }
  la = l.map { _1[0] }
  lb = l.map { _1[1] }

  la.sort.zip(lb.sort).map { (_1 - _2).abs }.sum
  # la.map { _1 * lb.count(_1) }.sum
end

result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
