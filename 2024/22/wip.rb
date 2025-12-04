def f(n, i) = (n ^ (n << i)) & ((1 << 24) - 1)
def secret(n) = f(f(f(n, 6), -5), 11)

def sequences(n)
  Enumerator.produce(n, &method(:secret)).take(2000).map { _1 % 10 }.each_cons(5)
            .each_with_object({}) { |nums, h| h[nums.each_cons(2).map { _2 - _1 }] ||= nums[4] }
end

input = File.read 'input.txt'
input = File.read 'input-sample.txt'
data = input.split("\n").map { _1.scan(/\d+/).map(&:to_i).first }
p(data.sum { |n| (0...2000).reduce(n) { secret(_1) } })

gains = data.map(&method(:sequences))
keys = gains.map(&:keys).flatten(1).to_set
p keys.map { |key| gains.sum { _1[key] || 0} }.max
