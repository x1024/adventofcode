#
# input = File.read 'input-sample.txt', encoding: 'utf-8'
input = File.read 'input.txt', encoding: 'utf-8'

def solve(((x1, y1), (x2, y2), (x, y)), lim)
  b = (x1*(y+lim) - y1*(x+lim)) / (x1*y2 - y1*x2)
  a = ((x+lim) - x2*b)/x1
  x1*a + x2*b == x+lim && y1*a + y2*b == y+lim ? a*3+b : 0
end

games = input.split("\n\n").map do |game|
  game.split("\n").map { |l| l.scan(/\d+/).map(&:to_i) }
end
p(games.sum { |d| solve(d, 0) })
p(games.sum { |d| solve(d, 10_000_000_000_000) })

require 'matrix'
eqs = File.read('input.txt').split("\n\n").map do
  _1.scan(/\d+/).map(&:to_i)
end.map { [Matrix[_1[0...2], _1[2...4]], Vector[*_1[4..]]] }
[0, 10**13].map { Vector[_1, _1] }.each do |o|
  p eqs.map { |m, v| m.t.lup.solve(v + o) }.select { _1.map(&:denominator).all?(1) }.sum { _1.dot [3, 1] }.to_i
end
