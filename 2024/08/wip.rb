input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

def check(data)
  seen = Set.new
  add = ->(pos) { seen.add(pos) if data.key?(pos) }
  data.to_a
      .select { |_, c| c.match?(/[a-zA-Z0-9]/) }
      .combination(2)
      .select { |(_, c1), (_, c2)| c1 == c2 }
      .map { |(p1, _), (p2, _)| [p1, p2, p2 - p1] }
      .each do |p1, p2, diff|
    p1 -= diff while add.(p1)
    p2 += diff while add.(p2)
  end
  seen.size
end

def main(input)
  data = input.split("\n").map.with_index do |line, x|
    line.each_char.map.with_index { |c, y| [x + y.i, c] }
  end.flatten(1).to_h

  check(data)
end

p main(input_sample)
p main(input_real)
