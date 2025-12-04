input = File.read 'input.txt', encoding: 'utf-8'
# input = File.read 'input-sample.txt', encoding: 'utf-8'

lines = input.split("\n")

la = []
lb = []
data = lines.map! do |line|
  a, b = line.split(' ').map(&:to_i)
  la.push a
  lb.push b
end

la.sort!
lb.sort!
p la, lb

result = 0
for i in 0..la.size - 1
  a = la[i]
  b = lb[i]
  result += p(a - b).abs
end

puts 'Result:', result

require 'clipboard'
Clipboard.copy result
