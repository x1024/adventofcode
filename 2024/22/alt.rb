def apply(n, *fns) = fns.reduce(n) { (_1 ^ _2.(_1)) & ((1<<24) - 1) }
def secrets(n) = Enumerator.produce(n) { |n| apply(n, -> { _1 * 64 }, -> { _1 / 32 }, -> { _1 * 2048 }) }

all = File.read('input.txt').lines.map(&:to_i).map { secrets(_1).take(2000) }
gains = Hash.new { |h, k| h[k] = [nil] * all.size }

all.each.with_index do |seq, monkey|
  seq.map { _1 % 10 }.each_cons(5) do |nums|
    diffs = nums.each_cons(2).map { _2 - _1 }
    gains[diffs][monkey] ||= nums[-1]
  end
end

p all.sum { _1[-1] }
p gains.values.map { _1.compact.sum }.max

pp gains.keys.size
