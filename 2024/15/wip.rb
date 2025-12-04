OFFSETS = { '<' => -1.i, '>' => +1.i, '^' => -1, 'v' => +1 }.freeze
TRANSFORM = { '#' => '##', 'O' => '[]', '@' => '@.', '.' => '..' }.freeze

def solve(input)
  map, moves = input.split("\n\n")
  moves = moves.split.join.chars.map { |c| OFFSETS[c] }
  map = map.split("\n").map.with_index do |line, x|
    line.each_char.map.with_index { |c, y| [x + y.i, c] }
  end.flatten(1).to_h

  @move = 0 + 0.i
  can_move = lambda do |pos|
    actor = map[pos]
    return false if actor == '#'
    return true if actor == '.'

    new_pos = pos + @move
    res = can_move.(new_pos)
    res &&= can_move.(new_pos + 1.i) if @move.real != 0 && actor == '['
    res &&= can_move.(new_pos - 1.i) if @move.real != 0 && actor == ']'
    res
  end

  do_move = lambda do |pos|
    actor = map[pos]
    return if '#.'.include? actor

    new_pos = pos + @move
    do_move.(new_pos)
    if map[new_pos] == '.'
      map[new_pos] = map[pos]
      map[pos] = '.'
    end

    do_move.(pos + 1.i) if @move.real != 0 && actor == '['
    do_move.(pos - 1.i) if @move.real != 0 && actor == ']'
  end

  robot = map.keys.find { |k| map[k] == '@' }
  moves.each do |m|
    @move = m
    next unless can_move.(robot)

    do_move.(robot)
    robot += @move
  end

  map.sum { |k, v| (k.real * 100 + k.imaginary) * ('O['.include?(v) ? 1 : 0) }
end

input = File.read 'input.txt', encoding: 'utf-8'

p solve(input)
p solve(input.chars.map { |k| TRANSFORM.fetch(k, k) }.join)
