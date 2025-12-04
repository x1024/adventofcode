input = File.read 'input.txt', encoding: 'utf-8'

def ordered(page, rules) = page.each_with_object([]) do |a, arr|
  arr[(rules[a] || []).count { page.include?(_1) }] = a
end.reverse

rules, pages = input.split("\n\n")
rules = rules.lines.map { _1.scan(/\d+/).map(&:to_i) }.group_by(&:first).transform_values { _1.flat_map(&:last).to_set }

p pages
  .lines.map { _1.scan(/\d+/).map(&:to_i) }
  .map { |page| [ordered(page, rules), page] }
  .partition { _1 == _2 }
  .map { _1.sum { |p, _| p[(p.count - 1) / 2] } }
