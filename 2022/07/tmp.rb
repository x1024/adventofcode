require 'pathname'

cwd = Pathname('/')
sizes = {cwd => 0}

File.read('input.txt').lines.each do |line|
  case line
  when /^\$ cd (.*)/ then cwd /= $1
  when /^dir (.*)/ then sizes[cwd / $1] = 0
  when /^(\d+) (.*)$/ then sizes[cwd / $2] = $1.to_i
  when /^\$ ls\s*$/
  else raise line
  end
end

dirs = sizes.filter { _2 == 0 }.to_h { |path,| [path, sizes.filter { _1.to_s.start_with? "#{path}/".gsub('//', '/') }.sum { _2 }] }

delta = dirs[Pathname('/')] - 40000000

p dirs.values.filter { _1 <= 100_000 }.sum
p dirs.values.filter { _1 >= delta }.min
