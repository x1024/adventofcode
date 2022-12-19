valves = File.read('input.txt').lines.to_h do |line|
  (line =~ /Valve (\S+) has flow rate=(\d+); .* to valves? (.*)/) or raise line
  [$1, {rate: $2.to_i, to: $3.split(', ')}]
end

def flow(open, valves) = open.uniq.map { |k| valves[k][:rate] }.sum

def go(time, one, two, score, seen, open, valves, move_one, &)
  return if seen.fetch([one, two, time], -1) >= score
  seen[[one, two, time]] = score

  yield score if time == 1
  return if time == 1

  if move_one
    possible = valves[one][:to].map { [_1, open] }
    possible.unshift [one, open + [one]] unless open.include?(one) or valves[one][:rate].zero?
  else
    possible = [[one, open]]
  end

  possible.each do |one, open|
    if not open.include?(two) and valves[two][:rate] > 0
      go(time - 1, one, two, score + flow(open + [two], valves), seen, open + [two], valves, move_one, &)
    end

    valves[two][:to].each do |two|
      go(time - 1, one, two, score + flow(open, valves), seen, open, valves, move_one, &)
    end
  end
end

p enum_for(:go, 30, 'AA', 'AA', 0, {}, [], valves, false).max
p enum_for(:go, 26, 'AA', 'AA', 0, {}, [], valves, true).max