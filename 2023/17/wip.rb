require "rb_heap"

seen = {}

heap = Heap.new { |a, b| a[2] < b[2] }
heap << [0i, -1+0i, 0, {}]

rmax = grid.keys.map(&:real).max
imax = grid.keys.map(&:imag).max

target = rmax + imax.i

until heap.empty?
  pos, dir, loss, path = heap.pop

  if pos == target
    p path
    p loss
    $min = loss
    $solve = path
    break
  end

  next if seen[[pos, dir]]
  seen[[pos, dir]] = true


  [1i, -1, -1i].each do |turn|
    next if loss == 0 && turn != -1
    next if loss > 0 && turn == -1

    new_dir = turn * dir

    new_pos = pos
    new_loss = loss
    new_path = path.dup

    steps = 0
    10.times do
      steps += 1
      new_pos += new_dir
      new_path[new_pos] = new_dir

      next unless grid[new_pos]
      new_loss += grid[new_pos]

      next if steps < 4

      #p [new_pos, new_dir, new_loss]
      heap << [new_pos, new_dir, new_loss, new_path.dup]
    end
  end
end
