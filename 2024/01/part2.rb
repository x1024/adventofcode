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
  cnt = 0
  for j in 0..lb.size - 1
    b = lb[j]
    cnt += 1 if a == b
  end
  result += cnt * a
end

puts 'Result:', result

require 'clipboard'
Clipboard.copy result
