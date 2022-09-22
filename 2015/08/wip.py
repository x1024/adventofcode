input = open('input.txt', 'r').read().strip()

lines = input.split('\n')

def count(row):
  row_encoded = '"' + row.replace('\\', '\\\\').replace('"', '\\"') + '"'
  return len(row_encoded) - len(row)

result = sum(count(row) for row in lines)
print("Result: {}".format(result))

