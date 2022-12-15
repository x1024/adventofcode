import numpy


def add(a, b):
  return tuple(a + b for (a, b) in zip(a, b))


def move_tail(rope):
  for i in range(1, len(rope)):
    delta = add(rope[i - 1], numpy.negative(rope[i]))
    if max(map(abs, delta)) >= 2: # If a tail is 2+ cells away from the head
      rope[i] = add(rope[i], map(numpy.sign, delta)) # Move the tail towards the head


def solve(data, rope_len=10):
  rope = [(0, 0)] * rope_len
  seen = set()
  for move in data:
    rope[0] = add(rope[0], move)
    move_tail(rope)
    seen.add(rope[-1])
  return len(seen)


dirs = {
  'U': (-1, 0),
  'D': (+1, 0),
  'L': (0, -1),
  'R': (0, +1),
}

input = open('input.txt', 'r').read().strip()
input = [row.split() for row in input.split('\n')]
input = [[dirs[dir]] * int(count) for (dir, count) in input]
input = sum(input, [])
print(solve(input, 2))
print(solve(input, 10))
