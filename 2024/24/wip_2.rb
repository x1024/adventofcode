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

def main(input)
  rules = input.split("\n\n").last.split("\n").map { |l| l.split(' -> ').then { [parse(_1), _2] } }.to_h

  renamed = {}
  rename = lambda do |key, to|
    from = rules[key]
    renamed[from] = to
    renamed[to] = from
    p [key, from, to]
    rules = rules.map do
      [parse(_1.gsub(from, to)), _2.gsub(from, to)]
    end.to_h
    File.write('renamed.txt', rules.map { |k, v| "#{k} -> #{v}" }.join("\n"))
  end

  # When any of this crashes, we have a swapped variable.
  # Just use your brain to figure out which one.
  # Fix it in the input, write it down, then proceed forward
  bits = 44
  (0..bits).each do |i|
    j = i.to_s.rjust(2, '0')
    rename.("x#{j} AND y#{j}", "AND_#{j}")
    rename.("x#{j} XOR y#{j}", "XOR_#{j}")
  end

  # first bit is special
  rename.('x00 XOR y00', 'z00')
  rename.('x00 AND y00', 'CARRY_00')

  check = lambda do |val, type|
    definition = rules.invert[val]
    p [val, definition, type]
  end

  (1..bits).each do |i|
    j = i.to_s.rjust(2, '0')
    j2 = (i-1).to_s.rjust(2, '0')
    begin
      rename.("CARRY_#{j2} AND XOR_#{j}", "TMP_#{j}")
    rescue TypeError
      p "CARRY_#{j2}, #{renamed["CARRY_#{j2}"]}"
      exit
    end
    begin
      renamOP = { 'AND' => :&, 'OR' => :|, 'XOR' => :^ }
      first, second = File.read('input.txt').split("\n\n")
      $inputs = first.lines.map { _1.chomp.split(': ') }.map { [_1.to_sym, _2.to_i] }.to_h
      $gates = second.lines.map { _1.chomp.split }.map { [_5.to_sym, [_1.to_sym, OP[_2], _3.to_sym]] }.to_h
      $inputs.keys.each { |k| define_method(k) { $inputs[k] } }
      $gates.keys.each { |k| define_method(k) { $gates[k].then { |a, op, b| send(a).send(op, send(b)) } } }
      $xs = $inputs.keys.grep(/^x/).sort
      $ys = $inputs.keys.grep(/^y/).sort
      $zs = $gates.keys.grep(/^z/).sort

      def value(names) = names.map { send _1 }.reverse.join.to_i(2)

      def score
        begin
          (value($xs) + value($ys)).digits(2).zip(value($zs).digits(2)).take_while { _1 == _2 }.count
        rescue StandardError
          0
        end
      rescue SystemStackError
        0
      end

      def random_score
        before = $inputs
        $inputs = $inputs.transform_values { rand(2) }
        $inputs[:x44] = $inputs[:y44] = 1
        score
      ensure
        $inputs = before
      end

      def seek(min = 0, swaps = [])
        if min >= $xs.size
          puts swaps.sort.join(',')
          exit
        end

        $gates.keys.combination(2) do |a, b|
          $gates[a], $gates[b] = $gates[b], $gates[a]
          seek(score, (swaps + [a, b]).sort) if score > min && 10.times.map { random_score }.min > min
          $gates[a], $gates[b] = $gates[b], $gates[a]
        end
      end

      p value $zs
      seek scoree.("AND_#{j} OR TMP_#{j}", "CARRY_#{j}")
    rescue TypeError
      p "TMP_#{j}, #{renamed["TMP_#{j}"]}"
      check.("TMP_#{j}", 'TMP')
      p "AND_#{j}, #{renamed["AND_#{j}"]}"
      check.("AND_#{j}", 'AND')
      exit
    end
  end

  # If we got here, then all bits are now good.
  # The gates you wrote down are the answer
end

input = File.read 'input.txt'
p part1(input)
# exit
main(input)
p %w[z06 jmq z13 gmh rqf cbd z38 qrh].sort.join(',')
require 'clipboard'
Clipboard.copy result
