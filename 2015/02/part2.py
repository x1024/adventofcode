input = open('input.txt', 'r').read().strip().split("\n")

result = 0
for row in input:
  l, w, h = sorted(map(int, row.split('x')))
  result += 2*(l+w) + l*w*h
print("Result: {}".format(result))
