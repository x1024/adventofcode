input = open('input.txt', 'r').read().strip()
lines = input.split('\n')

def count(row_big):
  return len(row_big) - len(eval(row_big))

result = sum(count(row) for row in lines)
print("Result: {}".format(result))

