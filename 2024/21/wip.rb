NUMS = {
  'A' => ['<0', '^3'],
  '0' => ['^2', '>A'],
  '1' => ['>2', '^4'],
  '2' => ['<1', '>3', '^5', 'v0'],
  '3' => ['<2', '^6', 'vA'],
  '4' => ['>5', 'v1', '^7'],
  '5' => ['<4', '>6', 'v2', '^8'],
  '6' => ['<5', 'v3', '^9'],
  '7' => ['>8', 'v4'],
  '8' => ['<7', '>9', 'v5'],
  '9' => ['<8', 'v6']
}.freeze

ARROWS = {
  'A' => ['v>', '<^'],
  '^' => ['>A', 'vv'],
  '>' => ['^A', '<v'],
  'v' => ['>>', '^^', '<<'],
  '<' => ['>v']
}.freeze

# Find all shortest paths from start to finish on the given keypad
def paths(start, finish, keypad)
  paths = []
  q = [[start, '']]
  while ((pos, path) = q.shift)
    next if paths[0]&.size&.< path.size

    q += keypad[pos].map { [_1[1], path + _1[0]] }
    paths << "#{path}A" if pos == finish
  end

  paths
end

def solve(line, limit, level = limit)
  # This is the last robot, the answer is just its program
  return line.size if level == 0

  # The shortest path is a sum of shortest paths.
  # Split the path into single steps, solve for each separately, sum the results
  ($memo ||= {})[[line, level]] ||= "A#{line}".chars.each_cons(2).map do |a, b|
    # Find all ways to solve this part
    # Then for each path, simulate it with the next robot, and get the best result
    keypad = level == limit ? NUMS : ARROWS
    paths(a, b, keypad).map { solve(_1, limit, level - 1) }.min
  end.sum
end

input = File.read('input.txt').split("\n").map { [_1, _1.gsub(/A/, '').to_i] }
p input.sum { solve(_1, 3) * _2 }
p input.sum { solve(_1, 26) * _2 }
