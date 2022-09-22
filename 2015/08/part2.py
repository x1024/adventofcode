input = open('input.txt', 'r').read().strip()

lines = input.split('\n')

def count(row):
  row_encoded = '"' + row.replace('\\', '\\\\').replace('"', '\\"') + '"'
  print row, row_encoded, len(row), len(row_encoded)
  return len(row_encoded) - len(row)

print lines
result = sum(count(row) for row in lines)
print("Result: {}".format(result))

