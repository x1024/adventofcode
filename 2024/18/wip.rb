def bfs(lines, size = 70, start = 0 + 0.i)
  data = Hash.new(nil).update(lines.to_h { [_1, 0] }).update(start => 0)
  q = [start]
  while (now = q.shift)
    return data[now] if now == size + size.i

    q += [1, -1, 1.i, -1.i]
         .map { now + _1 }
         .filter { _1.real.between?(0, size) && _1.imag.between?(0, size) && data[_1].nil? }
         .each { data[_1] = data[now] + 1 }
  end
end

lines = File.read('input.txt').split("\n").map { |l| l.scan(/\d+/).map(&:to_i).each_slice(2).sum { _1 + _2.i } }
a = bfs(lines[0...1024])
b = lines[(0...lines.size).bsearch { bfs(lines[0..._1]).nil? }-1]
p "#{a} #{b.real},#{b.imag}"
