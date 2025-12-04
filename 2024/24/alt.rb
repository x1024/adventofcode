OP = { 'AND' => :&, 'OR' => :|, 'XOR' => :^ }
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
seek score
