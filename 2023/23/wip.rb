grid = File.read('input.txt').lines.flat_map.with_index { |l, y| l.chomp.chars.map.with_index { [_2 + y.i, _1] } }.to_h

grid.each do |key, value|
  grid[key] = '.' unless value == '#'
end

target = grid.keys.max_by(&:abs2) - 1

start = 1 + 0i
choices = {}
choices[1 + 0i] = {}

grid.keys.each do |pos|
  next if grid[pos] != '.'
  opts = [1, -1, 1i, -1i].map { pos + _1 }.select { grid[_1] == '.' }
  next if opts.size <= 2
  choices[pos] = {}
end


choices.each do |key, opts|
  left = [[key, 0]]
  seen = {}

  until left.empty?
    pos, count = left.pop

    next if grid[pos] == '#' || grid[pos].nil?
    next if seen[pos]

    if pos == target
      opts[target] = count
      next
    end

    if choices[pos] && pos != key
      opts[pos] = count
      next
    end

    seen[pos] = true

    dirs = [1, -1, 1i, -1i]
    neis = dirs.map { |d| pos + d }.reject { grid[_1].nil? || grid[_1] == '#' || seen[_1] }

    neis.each do |nei|
      left << [nei, count + 1]
    end
  end
end

left = [[start, 0, []]]

max = 0
until left.empty?
  pos, count, path = left.pop

  if pos == target
    puts max
    max = [count, max].max
    next
  end

  path = path + [pos]

  choices[pos].each do |key, value|
    next if path.include? key
    left << [key, count + value, path]
  end
end

say max
