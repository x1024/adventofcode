input = open('input.txt', 'r').read().strip()
lines = input.split('\n')

data = []
for x in range(1000):
  data.append([0] * 1000)

for line in lines:
  words = line.split(" ")
  toggle = False
  if len(words) == 4:
    toggle = True
    words = [''] + words
  else:
    if words[1] == 'on':
      val = 1
    else:
      val = 0

  x0, y0 = map(int, words[2].split(","))
  x1, y1 = map(int, words[4].split(","))
  # print x0, y0, x1, y1
  for x in range(x0, x1+1):
    for y in range(y0, y1+1):
      if toggle:
        data[x][y] += 2
      else:
        if val == 1:
          data[x][y] += 1
        else:
          data[x][y] = max(0, data[x][y] - 1)

total = 0
for x in range(1000):
  for y in range(1000):
    total += data[x][y]

result = total
print("Result: {}".format(result))
