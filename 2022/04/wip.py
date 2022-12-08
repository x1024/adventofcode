def easy(input):
  return sum((a[0] <= b[0] and a[1] >= b[1]) or (b[0] <= a[0] and b[1] >= a[1])
    for a, b in input)


def hard(input):
  return sum(max(a[0], b[0]) <= min(a[1], b[1])
    for a, b in input)


def parse_line(line):
  return [list(map(int,c.split('-'))) for c in line.split(',')]


input = open('input.txt', 'r').read().strip()
input = [parse_line(line) for line in input.split("\n") if line]

print(easy(input))
print(hard(input))