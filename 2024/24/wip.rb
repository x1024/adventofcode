def part1(input)
  pa, pb = input.split("\n\n")
  start = pa.split("\n").map do |l|
    x, y = l.split(':')
    [x, y.to_i]
  end.to_h

  rules = pb.split("\n").map do |l|
    rule, res = l.split(' -> ')
    a, op, b = rule.split(' ')
    a, b = [a, b].sort
    [a, op, b, res]
  end
  while rules.any?
    rules.each do |rule|
      a, op, b, res = rule
      next unless start[a] && start[b]

      start[res] = case op
                   when 'AND'
                     start[a] & start[b]
                   when 'OR'
                     start[a] | start[b]
                   when 'XOR'
                     start[a] ^ start[b]
                   end
      rules.delete rule
    end
  end

  start.filter { _1.start_with? 'z' }.sort_by(&:first).map(&:last).join.reverse.to_i(2)
end

def parse(rule)
  a, op, b = rule.split(' ')
  "#{[a, b].min} #{op} #{[a, b].max}"
end

def part2(input)
  rules = input.split("\n\n").last.split("\n").map { |l| l.split(' -> ').then { [parse(_1), _2] } }.to_h
  vars = {}
  types = {}

  swaps = []
  swap = lambda do |a, b|
    k1 = rules.invert[a]
    k2 = rules.invert[b]
    rules[k1] = b
    rules[k2] = a
    types[a], types[b] = types[b], types[a]
    swaps << a
    swaps << b
    # p "swapped #{a} with #{b}"
    throw :swap
  end

  valid = lambda do |val, type|
    types[val] == type
  end

  rule = lambda { |typea, op, typeb|
    a = vars[typea]
    b = vars[typeb]
    r = rules["#{a} #{op} #{b}"] || rules["#{b} #{op} #{a}"]

    unless r
      # p [a, b, typea, typeb]
      # p ['!!!!', a, valid.(a, typea), valid.(b, typeb), b]
      if valid.(a, typea)
        other = rules.find { _1[0].include? a}.first.gsub(/ \w+ /, '').gsub(a, '')
        # p [a, b, other]
        swap.(b, other)
      else
        other = rules.find { _1[0].include? b}.first.gsub(/ \w+ /, '').gsub(b, '')
        # p [a, b, other]
        swap.(a, other)
      end

      throw :wat
    end

    r
  }

  bits = 44

  (0..bits).map { _1.to_s.rjust(2, '0') }.each do |i|
    types["x#{i}"] = 'x'
    types["y#{i}"] = 'y'
    types["z#{i}"] = 'z'
  end

  4.times do
    vars = {}
    vars['x'] = 'x00'
    vars['y'] = 'y00'
    vars['z'] = rule.('x', 'XOR', 'y')
    vars['carry'] = rule.('x', 'AND', 'y')
    # p vars.map { "#{_1[0]}: #{_1[1]}" }.join(', ')

    (1..44).each do |i|
      # p i
      j = i.to_s.rjust(2, '0')
      vars['x'] = "x#{j}"
      vars['y'] = "y#{j}"
      # p [i, 'xor']
      vars['xor'] = rule.('x', 'XOR', 'y')
      types[vars['xor']] ||= 'xor'

      # p [i, 'and']
      vars['and'] = rule.('x', 'AND', 'y')
      types[vars['and']] ||= 'and'

      # p [i, 'tmp']
      vars['tmp'] = rule.('carry', 'AND', 'xor')
      types[vars['tmp']] ||= 'tmp'

      # p [i, 'carry']
      vars['carry'] = rule.('and', 'OR', 'tmp')
      types[vars['carry']] ||= 'carry'

      # p vars.map { "#{_1[0]}: #{_1[1]}" }.join(', ')
    end
  rescue StandardError
  end

  swaps.sort.join(',')
end

input = File.read 'input.txt'
p part1(input)
p part2(input)
p %w[z06 jmq z13 gmh rqf cbd z38 qrh].sort.join(',')
