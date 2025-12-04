$best = []
$seen = Set.new
def solve(found, a)
  asd = (found.to_a + [a]).sort
  return 0 if $seen.include? asd

  $seen << asd

  $best = asd if found.size + 1 > $best.size
  # p [found.size + 1, (found.to_a + [a]).sort.join(',')]
  next_pcs = $connections[a]
             .filter { |c| !found.include? c }
             .filter { |c| found.all? { |f| $connections[f].include? c } }
  next_pcs.map { |c| solve(found + [a], c) }.sum
end

def main(input)
  lines = input.split("\n")

  $connections = {}
  data = lines.map do |line|
    a, b = line.split('-')
    $connections[a] ||= []
    $connections[b] ||= []
    $connections[a] << b
    $connections[b] << a
  end

  all = $connections.keys
  all.map do |a|
    solve(Set.new, a)
  end
  $best.join(',')
end

input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'
result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
