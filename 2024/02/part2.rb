input_real = File.read 'input.txt', encoding: 'utf-8'
input_sample = File.read 'input-sample.txt', encoding: 'utf-8'

def check(a)
  last = a[0]
  safe = true
  dir = if a[1] > a[0]
          1
        else
          -1
        end
  for i in 1..a.size - 1
    diff = a[i] - last
    safe = false if diff.abs > 3 || diff.abs < 1
    dir2 = if diff > 0
             1
           else
             -1
           end
    safe = false if dir2 != dir
    last = a[i]
  end
  safe
end

def main(input)
  l = input.split("\n").map { _1.scan(/\d+/).map(&:to_i) }

  l.map do |a|
    (0..a.size - 1).map do |i|
      check a[...i] + a[i + 1..]
    end.any?
  end.filter { |a| a }.count
end

result = main(input_sample)
p result
result = main(input_real)
p result
require 'clipboard'
Clipboard.copy result
