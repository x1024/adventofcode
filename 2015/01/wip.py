input = open('input.txt', 'r').read().strip()

result = 0
for c in input:
  if c == '(':
    result += 1
  if c == ')':
    result -= 1
print("Result: {}".format(result))

index = 0
result = 0
for c in input:
  index += 1
  if c == '(':
    result += 1
  if c == ')':
    result -= 1
  if result < 0:
    print(index)
    exit()

