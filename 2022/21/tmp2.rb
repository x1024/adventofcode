eval File.read('input.txt').gsub(/^(\w+): /, 'def \1() =')
puts root

exprs = File.read('input.txt').lines.to_h { _1.chomp.split(': ') }
target, answer = exprs['root'].split(' ')[0], eval(exprs['root'].split[2])

def humn() = raise

while target != 'humn'
  vals = exprs[target].split.then { |x| [x[1].to_sym, (eval(x[0]) rescue x[0]), (eval(x[2]) rescue x[2])] }
  puts "#{target} #{answer} #{exprs[target]} #{vals}"

  case exprs[target].split.then { |x| [x[1].to_sym, (eval(x[0]) rescue x[0]), (eval(x[2]) rescue x[2])] }
  in :+, *args then answer, target = args.sort_by { _1.class.name }.then { [answer - _1, _2] }
  in :-, Integer => a, target then answer = a - answer
  in :-, target, Integer => a then answer = answer + a
  in :*, *args then answer, target = args.sort_by { _1.class.name }.then { [answer / _1, _2] }
  in :/, Integer => a, target then answer = a / answer
  in :/, target, Integer => a then answer *= a
  end
end

p answer
