require 'set'

SHAPES = [[0, 1, 2, 3], [1, 1i, 1+1i, 2+1i, 1+2i], [0, 1, 2, 2+1i, 2+2i], [0, 1i, 2i, 3i], [0, 1, 1i, 1+1i]]

def move(dots, cave, dir) = dots.map { _1 + dir }.then { fits?(cave, _1) ? _1 : dots }
def fits?(cave, dots) = dots.all? { 0 <= _1.imag && (0..6).include?(_1.real) && !cave.include?(_1) }

tick, rock, cave, max, seen, done, wind = 0, nil, Set[], -1, {}, nil, File.read('input.txt').chomp.chars.map { _1.ord - 61 }

wind.each.with_index.cycle.each do |delta, beat|
  rock, tick = SHAPES[tick % SHAPES.size].map { _1 + max.i + 5i + 2 }, tick + 1 if rock.nil?
  rock = rock.then { move _1, cave, -1i }.then { move _1, cave, delta }

  next if move(rock, cave, -1i) != rock

  cave, max = cave + rock, [max, *rock.map(&:imag)].max
  rock, finger = nil, [tick % SHAPES.size, beat, [*0..30].product([*0..6]).map { cave.member? max.i - _1.i + _2 }]

  if done
    done[0] -= 1
    puts "Part 2: #{max + 1 + done[1]}" if done[0] == 0
    exit if done[0] <= 0 && tick > 2022
  elsif match = seen[finger]
    puts tick
    puts match[0]
    puts tick - match[0]
    height, left = (10**12 - tick).divmod(tick - match[0])
    done = [left, height * (max + 1 - match[1])]
  end

  seen[finger] = [tick, max + 1]
  puts "Part 1: #{max + 1}" if tick == 2022
end
