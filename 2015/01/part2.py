input = open('input.txt', 'r').read().strip()

index = 0
result = 0
for c in input:
  index += 1
  if c == '(':
    result += 1
  if c == ')':
    result -= 1
  if result < 0:
    print("Result: {}".format(index))
    exit()
