run_step = ->(a) { (~((a ^ 0b110) ^ (a >> ((a ^ 0b110) & 0b111)))) & 0b111 }
input = File.read('input.txt', encoding: 'utf-8').scan(/\d+/).map(&:to_i)

a1 = input[0]
p (0..a1.bit_length).step(3).map { run_step.(a1 >> _1) }.join(',')
p(input[3..].reverse.reduce([0]) do |options, opcode|
  options.map do |a|
    (0...8).map { (a << 3) + _1 }.filter { run_step.(_1) == opcode }
  end.flatten
end.first)
