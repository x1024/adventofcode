input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

# Task description:
=begin
--- Day 13: Claw Contraption ---

Next up: the lobby of a resort on a tropical island. The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade! Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual. Instead of a joystick or directional buttons to control the claw, these machines have two buttons labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured to move the claw a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend to win as many prizes as possible? You assemble a list of every machine's button behavior and prize location (your puzzle input). For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279

This list describes the button configuration and prize location of four different claw machines.

For now, consider just the first claw machine in the list:

Pushing the machine's A button would move the claw 94 units along the X axis and 34 units along the Y axis.
Pushing the B button would move the claw 22 units along the X axis and 67 units along the Y axis.
The prize is located at X=8400, Y=5400; this means that from the claw's initial position, it would need to move exactly 8400 units along the X axis and exactly 5400 units along the Y axis to be perfectly aligned with the prize in this machine.

The cheapest way to win the prize is by pushing the A button 80 times and the B button 40 times. This would line up the claw along the X axis (because 80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses, a total of 280 tokens.

For the second and fourth claw machines, there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing the A button 38 times and the B button 86 times. Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two; the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
=end

def solve2(line)
  x_a, y_a = line[0]
  x_b, y_b = line[1]
  prize_x, prize_y = line[2]
  a = 0
  answers = []
  # 28753
  (0..100).each do |a|
    (0..100).each do |b|
      if x_a * a + x_b * b == prize_x && y_a * a + y_b * b == prize_y
        answers << a * 3 + b
        p ['answer', a*3 + b, a, b]
      end
    end
  end
  return 0 if answers.empty?

  answers.min
end

def solve(line)
  x_a, y_a = line[0]
  x_b, y_b = line[1]
  prize_x, prize_y = line[2]
  # prize_x += 10_000_000_000_000
  # prize_y += 10_000_000_000_000

  a = 0
  answers = []
  # 28753
  # (0..100).each do |a|
  #  (0..100).each do |b|
  #    answers << a * 3 + b if x_a * a + x_b * b == prize_x && y_a * a + y_b * b == prize_y
  #  end
  # end
  # if answers.empty?
  #  return 0
  # end
  # return answers.min

  while true
    p1_x = prize_x - x_a * a
    p1_y = prize_y - y_a * a
    b = p1_x / x_b
    dist_x = prize_x - (x_a * a + x_b * b)
    dist_y = prize_y - (y_a * a + y_b * b)
    # p [dist_x, dist_y]
    answers << a * 3 + b if dist_x == 0 && dist_y == 0 && a <= 100 && b <= 100 && a >= 0 && b >= 0
    a += 1

    next unless a > 100

    return 0 if answers.empty?

    # p [answers, answers.min]
    return answers.min
  end
end

# LIM = 0
LIM = 10_000_000_000_000

def solve3(line)
  x_a, y_a = line[0]
  x_b, y_b = line[1]
  prize_x, prize_y = line[2]
  prize_x += LIM
  prize_y += LIM
  # p ['-----', prize_x, prize_y]
  check = lambda { |a|
    p1_x = prize_x - x_a * a
    p1_y = prize_y - y_a * a
    b = p1_x / x_b
    dist_x = prize_x - (x_a * a + x_b * b)
    dist_y = prize_y - (y_a * a + y_b * b)
    p [a, dist_x, dist_y]
    dist_y >= 0
  }
  check2 = lambda { |a|
    p1_x = prize_x - x_a * a
    p1_y = prize_y - y_a * a
    b = p1_x / x_b
    dist_x = prize_x - (x_a * a + x_b * b)
    dist_y = prize_y - (y_a * a + y_b * b)
    p [a, dist_x, dist_y]
    dist_y
  }

  p 'asdasd'
  p check2.(0)
  p check2.(LIM + 100)
  range = if check2.(0) < check2.(LIM + 100)
            (0..(LIM + 100))
          else
            (LIM..0)
          end

  a = range.bsearch { |a| check.(a) }

  return 0 if a.nil?

  p1_x = prize_x - x_a * a
  p1_y = prize_y - y_a * a
  b = p1_x / x_b
  return a * 3 + b if x_a * a + x_b * b == prize_x && y_a * a + y_b * b == prize_y

  0
end

def solve4(line)
  x1, y1 = line[0]
  x2, y2 = line[1]
  x, y = line[2]
  x += LIM
  y += LIM

  b = (x1*y - y1*x) / (x1*y2 - y1*x2)
  a = (x - x2*b)/x1
  # p [a, b, a*3+b]
  return 0 unless x1*a + x2*b == x && y1*a + y2*b == y

  # a*3+b
  if a >= 0 && b >= 0 && a <= LIM+100 && b <= LIM+100
    a*3+b
  else
    0
  end
end

def main(input)
  lines = input.split("\n\n")

  data = lines.map do |line|
    line.split("\n").map do |l|
      l.scan(/\d+/).map(&:to_i)
    end
  end
  # data = data[1...2]
  # p data.size
  # data.sum { |d| solve(d) }
  data.sum do |d|
    solve4(d)
  end
end

#  p main(input_sample)
result = main(input_real)
p result
# require 'clipboard'
# Clipboard.copy result
