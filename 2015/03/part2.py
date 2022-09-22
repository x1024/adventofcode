input = open('input.txt', 'r').read().strip()

visited = set()
pos = (0, 0)
visited.add(pos)
print input[::2]
print input[1::2]

for c in input[::2]:
  if c == '^': offset = (-1, 0)
  if c == '<': offset = (0, 1)
  if c == '>': offset = (0, -1)
  if c == 'v': offset = (1, 0)
  pos = (pos[0] + offset[0], pos[1] + offset[1])
  print c, pos
  visited.add(pos)

pos = (0, 0)
for c in input[1::2]:
  if c == '^': offset = (-1, 0)
  if c == '<': offset = (0, 1)
  if c == '>': offset = (0, -1)
  if c == 'v': offset = (1, 0)
  pos = (pos[0] + offset[0], pos[1] + offset[1])
  print c, pos
  visited.add(pos)

result = len(visited)
print("Result: {}".format(result))