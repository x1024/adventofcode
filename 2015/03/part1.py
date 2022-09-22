input = open('input.txt', 'r').read().strip()
lines = input.split("\n")

visited = set()
pos = (0, 0)
visited.add(pos)
for c in input:
  visited.add(pos)
  if c == '^': offset = (-1, 0)
  if c == '<': offset = (0, 1)
  if c == '>': offset = (0, -1)
  if c == 'v': offset = (1, 0)
  pos = (pos[0] + offset[0], pos[1] + offset[1])

result = len(visited)
print("Result: {}".format(result))
