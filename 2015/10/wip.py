input = open('input.txt', 'r').read().strip()

def iterate(input):
  current = -1
  counter = 0
  total = []
  for c in input:
    c = int(c)
    if c == current:
      counter += 1
    else:
      if current > 0:
        total.append((counter, current))
      current = c
      counter = 1
  total.append((counter, current))
  return ''.join('%s%s' % (a, b) for (a, b) in total)

for i in range(50):
  input = iterate(input)
  print i, len(input)

result = 0
print("Result: {}".format(result))
