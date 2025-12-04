p(File.read('input.txt')
  .split("\n\n")
  .map(&:lines)
  .map { |b| [b[0], (0...5).map { |i| b.count { _1[i] == '#' } }] }
  .group_by(&:first)
  .transform_values { _1.map(&:last) }
  .values
  .reduce(&:product)
  .count { |key, lock| key.zip(lock).all? { _1 + _2 <= 7 } })
