path, map = File.read('input.txt').split("\n\n")
map = map.lines.map { _1.scan /\w{3}/ }.to_h { [_1, [_2, _3]] }
path = path.tr('LR', '01').chars.map(&:to_i)

initial = nodes = map.keys.grep(/A$/)
found = [nil] * nodes.size

path.cycle.with_index do |dir, steps|
  nodes.each_with_index { found[_2] ||= steps if _1.end_with?('Z') }
  break if found.all?
  nodes = nodes.map { map[_1][dir] }
end

p found[initial.find_index('AAA')]
p found.reduce(:lcm)
