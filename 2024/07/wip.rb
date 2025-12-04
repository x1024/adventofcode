def solve((expected, *line), operations)
  (solve2 = lambda do |acc, i|
    i == line.size ? acc == expected : operations.(acc, line[i]).any? {|res| solve2.(res, i+1)}
  end).(0, 0) ? expected : 0
end

input = File.read('input.txt', encoding: 'utf-8').lines.map {|line| line.scan(/\d+/).map(&:to_i)}
p(input.sum {|d| solve d, -> {[_1+_2, _1*_2] }})
p(input.sum {|d| solve d, -> {[_1+_2, _1*_2, "#{_1}#{_2}".to_i] }})
