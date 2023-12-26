mods = {}
lines.each do |line|
  from, to = line.split(' -> ')
  to = to.split(', ')
  type = ' '

  if from[0] == '%' || from[0] == '&'
    name, type = from[1..], from[0]
  else
    name = from
  end

  mods[name] = {type: type, to: to}

  to.each do |t|
    mods[t] ||= {type: ' ', to: []}
  end
end

messages = []
states = {}

mods.each do |mod, vals|
  if vals[:type] == '%' || vals[:type] == '&'
    states[mod] = 0
  end
end

incoming = {}

mods.each do |name, vals|
  vals[:to].each do |t|
    if mods[t][:type] == '&'
      incoming[t] ||= {}
      incoming[t][name] = 0
    end
  end
end


counts = {0 => 0, 1 => 0}

seen = {}

inc = %w[sg lm dh db]

last = {}

first = {}
count = 0
loop do
  count += 1
  puts "tick #{count}" if count % 10_000 == 0
  messages << ['broadcaster', 0, 'button']
  if seen[states]
    puts "Seen on #{count}"
    exit
  end

  seen[states.dup] = true
  #p incoming.values.map { _1.values.join }
  until messages.empty?
    target, pulse, from = messages.shift

    last[target] = pulse

    status = {}
    inc.each do
      status[_1] = last[_1]
      first[_1] ||= count if last[_1] == 0
    end

    if first.size == 4
      say first.values.reduce(:*)
      exit
    end


    if target == 'rx' && pulse == 0
      say count
      exit
    end

    #p states
    #p incoming
    #puts "#{from} #{pulse} -> #{target} / #{incoming[target].inspect} #{states[target]}"

    counts[pulse] += 1

    case mods[target][:type]
    when ' '
      next unless target == 'broadcaster'
      mods[target][:to].each do |t|
        messages << [t, pulse, target]
      end
    when '%'
      next if pulse == 1
      states[target] = 1 - states[target]
      mods[target][:to].each do |t|
        messages << [t, states[target], target]
      end
    when '&'
      incoming[target][from] = pulse
      to_send = incoming[target].values.all? { _1 == 1 } ? 0 : 1
      mods[target][:to].each do |t|
        messages << [t, to_send, target]
      end
    else
      raise "Unknown type #{mods[target][:type]}"
    end
  end
end

say counts.values.reduce(:*)

