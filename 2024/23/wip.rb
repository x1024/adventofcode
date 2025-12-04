conn = File.read('input.txt').split("\n")
           .map { |line| line.split('-').sort }
           .group_by(&:first)
           .to_h.transform_values { _1.map(&:last).sort }

solve = lambda do |cur|
  conn.fetch(cur[-1], [])
      .filter { |c| cur.all? { conn[_1].include? c } }
      .map { solve.(cur + [_1]) }
      .max_by(&:size) || cur
end

p(conn.flat_map { |a, links| links.combination(2).filter { conn[_1]&.include? _2 }.map { [a, _1, _2] } }
      .filter { |c| c.any? { _1.start_with? 't' } }.uniq.size)
p(conn.map { solve.([_1]) }.max_by(&:size).join(','))
