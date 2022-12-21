eval File.read('input.txt').gsub(/^(\w+):/, 'def \1()= ')
puts(File.read('input.txt').gsub(/^(\w+):/, 'def \1()= '))
puts root
