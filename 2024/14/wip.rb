# Store(and solve) each axis separately
axes = File.read('input.txt', encoding: 'utf-8').split("\n")
           .map { |line| line.scan(/-?\d+/).map(&:to_i) }
           .map { [[_1, _3], [_2, _4]] }
           .transpose
# size of each axis
moduli = [101, 103]

# run the simulation to a given time
sim = ->((pos, speed), time, mod) { (pos + speed * time) % mod }

# just set the simulation to 100 seconds and count the number of points that are on the same coordinate in each axis
# (excluding the middle parts)
p(axes.transpose
  .group_by { |row| row.zip(moduli).map { (sim.(_1, 100, _2) - _2 / 2) <=> 0 } }
  .map { _1.include?(0) ? 1 : _2.size }
  .reduce(:*))

# find the maximum number of points that are on the same coordinate in each axis
# (The target image has a square border)
# (The simulation on each axis is periodical by the size of the axis)
remainders = axes.zip(moduli).map do |(axis, mod)|
  (0..mod).max_by { |time| axis.group_by { sim.(_1, time, mod) }.map { _2.size }.max }
end

# Then simply solve the chinese remaider theorem for the given remainders and moduli
# https://codegolf.stackexchange.com/questions/48057/chinese-remainder-theorem
require('openssl')

mod = moduli.reduce(&:*)
p moduli.zip(remainders).sum { |a, b| (mod/a).to_bn.mod_exp(a.to_bn-2, a.to_bn).to_i*b*mod/a } % mod
