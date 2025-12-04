input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:
=begin
--- Day 21: Keypad Conundrum ---

As you teleport onto Santa's Reindeer-class starship, The Historians begin to panic: someone from their search party is missing. A quick life-form scan by the ship's computer reveals that when the missing Historian teleported, he arrived in another part of the ship.

The door to that area is locked, but the computer can't open it; it can only be opened by physically typing the door codes (your puzzle input) on the numeric keypad on the door.

The numeric keypad has four rows of buttons: 789, 456, 123, and finally an empty gap followed by 0A. Visually, they are arranged like this:

+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

Unfortunately, the area outside the door is currently depressurized and nobody can go near the door. A robot needs to be sent instead.

The robot has no problem navigating the ship and finding the numeric keypad, but it's not designed for button pushing: it can't be told to push a specific button directly. Instead, it has a robotic arm that can be controlled remotely via a directional keypad.

The directional keypad has two rows of buttons: a gap / ^ (up) / A (activate) on the first row and < (left) / v (down) / > (right) on the second row. Visually, they are arranged like this:

    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

When the robot arrives at the numeric keypad, its robotic arm is pointed at the A button in the bottom right corner. After that, this directional keypad remote control must be used to maneuver the robotic arm: the up / down / left / right buttons cause it to move its arm one button in that direction, and the A button causes the robot to briefly move forward, pressing the button being aimed at by the robotic arm.

For example, to make the robot type 029A on the numeric keypad, one sequence of inputs on the directional keypad you could use is:

< to move the arm from A (its initial position) to 0.
A to push the 0 button.
^A to move the arm to the 2 button and push it.
>^^A to move the arm to the 9 button and push it.
vvvA to move the arm to the A button and push it.

In total, there are three shortest possible sequences of button presses on this directional keypad that would cause the robot to type 029A: <A^A>^^AvvvA, <A^A^>^AvvvA, and <A^A^^>AvvvA.

Unfortunately, the area containing this directional keypad remote control is currently experiencing high levels of radiation and nobody can go near it. A robot needs to be sent instead.

When the robot arrives at the directional keypad, its robot arm is pointed at the A button in the upper right corner. After that, a second, different directional keypad remote control is used to control this robot (in the same way as the first robot, except that this one is typing on a directional keypad instead of a numeric keypad).

There are multiple shortest possible sequences of directional keypad button presses that would cause this robot to tell the first robot to type 029A on the door. One such sequence is v<<A>>^A<A>AvA<^AA>A<vAAA>^A.

Unfortunately, the area containing this second directional keypad remote control is currently -40 degrees! Another robot will need to be sent to type on that directional keypad, too.

There are many shortest possible sequences of directional keypad button presses that would cause this robot to tell the second robot to tell the first robot to eventually type 029A on the door. One such sequence is <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A.

Unfortunately, the area containing this third directional keypad remote control is currently full of Historians, so no robots can find a clear path there. Instead, you will have to type this sequence yourself.

Were you to choose this sequence of button presses, here are all of the buttons that would be pressed on your directional keypad, the two robots' directional keypads, and the numeric keypad:

<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
v<<A>>^A<A>AvA<^AA>A<vAAA>^A
<A^A>^^AvvvA
029A

In summary, there are the following keypads:

One directional keypad that you are using.
Two directional keypads that robots are using.
One numeric keypad (on a door) that a robot is using.

It is important to remember that these robots are not designed for button pushing. In particular, if a robot arm is ever aimed at a gap where no button is present on the keypad, even for an instant, the robot will panic unrecoverably. So, don't do that. All robots will initially aim at the keypad's A key, wherever it is.

To unlock the door, five codes will need to be typed on its numeric keypad. For example:

029A
980A
179A
456A
379A

For each of these, here is a shortest sequence of button presses you could type to cause the desired code to be typed on the numeric keypad:

029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A

The Historians are getting nervous; the ship computer doesn't remember whether the missing Historian is trapped in the area containing a giant electromagnet or molten lava. You'll need to make sure that for each of the five codes, you find the shortest sequence of button presses necessary.

The complexity of a single code (like 029A) is equal to the result of multiplying these two values:

The length of the shortest sequence of button presses you need to type on your directional keypad in order to cause the code to be typed on the numeric keypad; for 029A, this would be 68.
The numeric part of the code (ignoring leading zeroes); for 029A, this would be 29.

In the above example, complexity of the five codes can be found by calculating 68 * 29, 60 * 980, 68 * 179, 64 * 456, and 64 * 379. Adding these together produces 126384.

Find the fewest number of button presses you'll need to perform in order to cause the robot in front of the door to type each code. What is the sum of the complexities of the five codes on your list?
=end

def check(line)
  p line
  true
end

# keypad
# 7 8 9
# 4 5 6
# 1 2 3
# _ 0 A
KEYPAD = [
  %w[7 8 9],
  %w[4 5 6],
  %w[1 2 3],
  [nil, '0', 'A']
].map.with_index do |line, x|
  line.map.with_index { |c, y| [x + y.i, c] }
end.flatten(1).filter { |_, c| c }.to_h

KEYPAD_ROBOT = [
  [nil, '^', 'A'],
  ['<', 'v', '>']
].map.with_index do |line, x|
  line.map.with_index { |c, y| [x + y.i, c] }
end.flatten(1).filter { |_, c| c }.to_h

OFFSETS = {
  'v' => 1,
  '^' => -1,
  '<' => -1.i,
  '>' => 1.i
}.freeze

def move_score(moves)
  score = 0
  moves.gsub(/(.)(\1)/) do |m|
    score += 1
    m[0]
  end
  moves.gsub(/^/) do
    score += 2
    ''
  end
  moves.gsub(/>/) do
    score += 2
    ''
  end
  moves.gsub(/v/) do
    score += 4
    ''
  end
  moves.gsub(/</) do
    score += 4
    ''
  end
  score
  # moves = moves.replace('<<', '<').replace('>>', '>').replace('^^', '^').replace('vv', 'v')
end

def solve_keypad(start, moves_map)
  p1 = moves_map.find { |_, c| c == start }.first
  dists = { p1 => [''] }
  q = [p1]
  # p ['start', p1]
  while (pos = q.shift)
    d = dists[pos]
    # p pos
    OFFSETS.each do |c, offset|
      new = pos + offset
      # p ['new', new, d.size + 1, dists[new]&.first&.size]
      next unless moves_map.key?(new)
      next if dists[new]&.first&.size&.< d.size + 1

      q << new
      dists[new] ||= []
      d.each do |dd|
        dists[new] << dd + c
      end
    end
  end

  # pp start
  # pp dists
  # pp start, p1
  # exit
  dists.map do |k, v|
    ms = v.min { _1.size <=> _2.size }.size
    m = v.select {_1.size == ms}.map { _1 + 'A'}.to_set.to_a
    [moves_map[k], m]
  end.to_h
end

def shortest_path(a, b)
end

MOVES_KEYPAD = {}
%w[1 2 3 4 5 6 7 8 9 0 A].each do |start|
  all = solve_keypad(start, KEYPAD)
  all.each do |finish, moves|
    MOVES_KEYPAD[[start, finish]] = moves
  end
end

MOVES_ROBOT = {}
%w[v < > ^ A].each do |start|
  all = solve_keypad(start, KEYPAD_ROBOT)
  all.each do |finish, moves|
    MOVES_ROBOT[[start, finish]] = moves
  end
end

ASD_KEYPAD = {
  'A' => {
    '<' => '0',
    '^' => '3'
  },
  '0' => {
    '^' => '2',
    '>' => 'A'
  },
  '1' => {
    '>' => '2',
    '^' => '4'
  },
  '2' => {
    '<' => '1',
    '>' => '3',
    '^' => '5',
    'v' => '0'
  },
  '3' => {
    '<' => '2',
    '^' => '6',
    'v' => 'A'
  },
  '4' => {
    '>' => '5',
    'v' => '1',
    '^' => '7'
  },
  '5' => {
    '<' => '4',
    '>' => '6',
    'v' => '2',
    '^' => '8'
  },
  '6' => {
    '<' => '5',
    'v' => '3',
    '^' => '9'
  },
  '7' => {
    '>' => '8',
    'v' => '4'
  },
  '8' => {
    '<' => '7',
    '>' => '9',
    'v' => '5'
  },
  '9' => {
    '<' => '8',
    'v' => '6'
  }
}

ASD_ROBOT = {
  'A' => {
    'v' => '>',
    '<' => '^'
  },
  '^' => {
    '>' => 'A',
    'v' => 'v'
  },
  '>' => {
    '^' => 'A',
    '<' => 'v'
  },
  'v' => {
    '>' => '>',
    '^' => '^',
    '<' => '<'
  },
  '<' => {
    '>' => 'v'
  }
}
# def simulate(line, keypad, now = 'A')
#   line.chars.map do |c|
#     moves = keypad[[now, c]].first
#     now = c
#     moves
#   end.join
# end

def solve(line)
  # p 'solve', line
  now = 'A'
  all_moves = [line]

  all_moves = all_moves.map { simulate _1, MOVES_KEYPAD }
  # all_moves = all_moves.reduce { |a, b| a.product(b).map { _1 + _2 } }
  # all_moves = all_moves[0...1]
  p all_moves, all_moves.map(&:size)
  exit
  all_moves = all_moves.map { simulate _1, MOVES_ROBOT }
  p all_moves, all_moves[0].size

  all_moves = all_moves.map { simulate _1, MOVES_ROBOT }
  p all_moves, all_moves[0].size
  exit

  all_moves = all_moves.sum([]) do |line|
    line.chars.map do |c|
      moves = MOVES_ROBOT[[now, c]]
      now = c
      moves
    end
  end
  all_moves = all_moves.reduce { |a, b| a.product(b).map { _1 + _2 } }
  all_moves = all_moves[0...1]
  p all_moves
  exit

  all_moves = all_moves.sum([]) do |line|
    line.chars.map do |c|
      moves = MOVES_ROBOT[[now, c]]
      now = c
      moves
    end
  end
  all_moves = all_moves.reduce { |a, b| a.product(b).map { _1 + _2 } }
  all_moves = all_moves[0...1]
  # p all_moves

  # p all_moves, all_moves.size
  moves = all_moves[0]
  # p line.gsub(/A/, '').to_i
  res = line.gsub(/A/, '').to_i * moves.size
  # p [line, line.gsub(/A/, '').to_i, moves.size, res]
  p moves
  p [res, moves.size, line.gsub(/A/, '').to_i]
  res
end

def simulate0(text, robots, keypads, move)
  if move != 'A'
    keypad = keypads[robots.size - 1]
    new_pos = keypad[robots[-1]][move]
    # p [text, robots, keypads, move, new_pos]
    # new_pos = ASD_KEYPAD[robot1][move]
    return nil if new_pos.nil?

    new_robots = robots[0...-1] + [new_pos]
    # p ['new move', text, new_robots]
    return [text, new_robots]
  end

  if robots.size == 1
    [text + robots[0], robots]
  else
    new_state = simulate0(text, robots[0...-1], keypads, robots[-1])
    return nil if new_state.nil?

    new_text, new_robots = new_state
    [new_text, new_robots + [robots[-1]]]
  end
end

def simulate1(text, robot1, move)
  if move != 'A'
    new_pos = ASD_KEYPAD[robot1][move]
    return nil if new_pos.nil?

    return [text, new_pos]
  end

  [text + robot1, robot1]
end

def simulate2(text, robot1, robot2, move)
  if move != 'A'
    new_pos = ASD_ROBOT[robot2][move]
    return nil if new_pos.nil?

    return [text, robot1, new_pos]
  end

  new_state = simulate1(text, robot1, robot2)
  return nil if new_state.nil?

  new_text, new_robot1 = new_state
  [new_text, new_robot1, robot2]
end

def simulate3(text, robot1, robot2, robot3, move)
  if move != 'A'
    new_pos = ASD_ROBOT[robot3][move]
    return nil if new_pos.nil?

    return [text, robot1, robot2, new_pos]
  end

  new_state = simulate2(text, robot1, robot2, robot3)
  return nil if new_state.nil?

  new_text, new_robot1, new_robot2 = new_state
  [new_text, new_robot1, new_robot2, robot3]
end

def solve2(line)
  state = ['', 'A', 'A']
  q = [state]
  seen = {}
  dists = { state => '' }
  while (state = q.shift)
    # p ['state', state]
    next if seen.key?(state)

    seen[state] = true

    text, robot1, robot2 = state
    if line == text
      # p ['found', text, dists[state]]
      return dists[state]
    end
    next unless line.start_with?(text)

    # robot 2 move
    'v^<>A'.chars.each do |move|
      new_state = simulate2(text, robot1, robot2, move)
      next if new_state.nil?

      next unless dists[new_state].nil? || dists[new_state].size >= dists[state].size + 1

      # p ['move', move, new_state]

      dists[new_state] = dists[state] + move
      q << new_state
    end
  end
end

def solve1(line)
  state = ['', 'A']
  q = [state]
  seen = {}
  dists = { state => '' }
  while (state = q.shift)
    # p ['state', state]
    next if seen.key?(state)

    seen[state] = true

    text, robot1 = state
    if line == text
      # p ['found', text, dists[state]]
      return dists[state]
    end
    next unless line.start_with?(text)

    # robot 2 move
    'v^<>A'.chars.each do |move|
      new_state = simulate1(text, robot1, move)
      next if new_state.nil?

      next unless dists[new_state].nil? || dists[new_state].size >= dists[state].size + 1

      # p ['move', move, new_state]

      dists[new_state] = dists[state] + move
      q << new_state
    end
  end
end

def solve3(line)
  state = ['', 'A', 'A', 'A']
  q = [state]
  seen = {}
  dists = { state => '' }
  while (state = q.shift)
    # p ['state', state]
    next if seen.key?(state)

    seen[state] = true

    text, robot1, robot2, robot3 = state
    if line == text
      # p ['found', text, dists[state]]
      return dists[state]
    end
    next unless line.start_with?(text)

    # robot 2 move
    'v^<>A'.chars.each do |move|
      new_state = simulate3(text, robot1, robot2, robot3, move)
      next if new_state.nil?

      next unless dists[new_state].nil? || dists[new_state].size >= dists[state].size + 1

      # p ['move', move, new_state]

      dists[new_state] = dists[state] + move
      q << new_state
    end
  end
end

# def move_score(dist) end

$memo = {}
def solve0(line, keypads, state)
  key = [line, keypads, state]
  return $memo[key] if $memo.key?(key)

  # state = ['', keypads.map { 'A' }]
  q = [[state, '']]
  seen = {}
  paths = []
  while ((state, path) = q.shift)
    # pp dists
    # next if seen.key?(state)
    next if paths.size > 0 && path.size > paths[0].size.to_i

    # p ['state', state, path]

    seen[state] = true

    text, robots = state
    if line == text
      # p ['found', text, path]
      paths << path
      # return path
      next
    end
    next unless line.start_with?(text)

    # robot 2 move
    'A^>v<'.chars.each do |move|
      new_state = simulate0(text, robots, keypads, move)
      next if new_state.nil?

      new_path = path + move
      q << [new_state, new_path]
    end
  end

  $memo[key] = paths
  paths
end

LIMIT = 26
$memo2 = {}
def asdasd(line, i = 0)
  key = [line, i]
  return $memo2[key] if $memo2.key?(key)
  return line.size if i == LIMIT

  chars = ('A' + line).chars
  res = chars.each_cons(2).map do |a, b|
    keypads = i == 0 ? [ASD_KEYPAD] : [ASD_ROBOT]
    r2 = solve0(b, keypads, ['', [a]])
    r = r2.map do |r|
      asdasd(r, i + 1)
    end.min
    r
  end.sum
  $memo2[key] = res
  res
end

def main(input)
  lines = input.split("\n")
  p(lines.map do |line|
    res = asdasd(line)
    r2 = res * line.gsub(/A/, '').to_i
    p [line, res, r2]
    r2
  end.sum)
  exit
end

# result = main(input_sample)
# p result
result = main(input_real)
p result
# require 'clipboard'
# Clipboard.copy result
