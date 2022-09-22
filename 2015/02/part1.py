input = open('input.txt', 'r').read().strip().split("\n")

result = 0
for row in input:
  l, w, h = map(int, row.split('x'))
  result += 2*l*w + 2*w*h + 2*h*l
  result += min(l*w, w*h, h*l)
print("Result: {}".format(result))
