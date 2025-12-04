$graph = Hash.new { |k, v| k[v] = Set[] }
$found = Set[]

File.read('input.txt').lines.each do |line|
  a, b = line.chomp.split(?-)
  $graph[a].add b
  $graph[b].add a
end

def seek(set)
  return if $found.any? { set.subset? _1 }
  $found.add set

  $graph.each do |node, neis|
    next if set.include? node
    seek set.dup.tap { _1.add node } if set.subset? neis
  end
end

seek Set[]
puts $found.max_by(&:size).to_a.sort.join(?,)
