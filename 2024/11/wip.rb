def memoize(method_name)
  memo = {}
  old = method(method_name)
  define_method(method_name) do |*args|
    key = args.map(&:to_s).join('-')
    return memo[key] if memo[key]

    memo[key] = old.call(*args)
    memo[key]
  end
end

def evolve(s, t)
  return 1 if t <= 0
  return evolve('1', t - 1) if s.match(/^0+$/)

  if s.length.even?
    s.chars.each_slice(s.length/ 2).sum { |a| evolve(a.join.to_i.to_s, t-1) }
  else
    evolve((s.to_i * 2024).to_s, t - 1)
  end
end

memoize(:evolve)

p(File.read('input.txt', encoding: 'utf-8').scan(/\d+/).sum { |n| evolve(n, 75) })
