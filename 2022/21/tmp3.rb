eval File.read('input.txt').gsub(/^(\w+): /, 'def \1() =')
p root

class Proc
  def +(other) = -> { _1 == :solve ? call(other) : call(_1 - other.real) }
  def *(other) = -> { call _1 / other.real }
  def -(other) = -> { call other.real? ? other.real + _1 : other.real - _1 }
  def /(other) = -> { call other.real? ? other.real * _1 : other.real / _1 }
  def coerce(other) = [self, other + 0i]
end

def humn() = ->(x) { x }
p root.(:solve)

