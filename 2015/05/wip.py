input = open('input.txt', 'r').read().strip()
lines = input.split("\n")

nice = 0
vowels = 'aeiou'
for row in lines:
  good_a = False
  good_b = False
  for i in range(0, len(row) - 1):
    digraph = row[i] + row[i+1]
    if digraph in row[i+2:]:
      good_a = True
  for i in range(0, len(row) - 2):
    if row[i] == row[i+2]:
      good_b = True
  nice += good_a and good_b

result = nice
print("Result: {}".format(result))
