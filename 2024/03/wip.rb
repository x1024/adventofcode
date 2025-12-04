input = File.read 'input.txt', encoding: 'utf-8'

result = 0
enabled = true
input.scan(/mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))/) do |match|
  if match[2]
    enabled = true
  elsif match[3]
    enabled = false
  elsif enabled
    result += match[0].to_i * match[1].to_i
  end
end

p result
