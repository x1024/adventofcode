input = open('input.txt', 'r').read().strip()
lines = input.split("\n")
# lines = map(int, lines)

nice = 0
vowels = 'aeiou'
for row in lines:
  vc = 0
  repeat = False
  for i in range(0, len(row)):
    c = row[i]
    if c in vowels:
      vc += 1
    if i < len(row) - 1 and row[i] == row[i+1]:
      repeat = True

  bad = False
  for s in ['ab', 'cd', 'pq', 'xy']:
    if s in row:
      bad = True
  print row, vc >= 3, repeat, not bad
  if vc >= 3 and repeat and not bad:
    nice += 1

result = nice
print("Result: {}".format(result))
