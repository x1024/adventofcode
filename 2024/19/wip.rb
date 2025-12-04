towels, designs = File.read('input.txt').split("\n\n")
towels = towels.split(', ')
memo = { '' => 1 }

define_method :check do |design|
  memo[design] ||= towels.sum { design.start_with?(_1) ? check(design[_1.size..]) : 0 }
end
designs = designs.split("\n").map(&method(:check))

p [designs.count { _1 > 0 }, designs.sum]
