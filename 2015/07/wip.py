input = open('input.txt', 'r').read().strip()
lines = input.split('\n')

formulas = {}
for row in lines:
  inp, out = row.split(" -> ")
  out = out.strip()
  inp = inp.strip()
  inp = inp.split(' ')
  formulas[out] = inp

cache = {}
def solve(key):
  if key in cache:
    return cache[key]

  if key[0] in '0123456789':
    print key
    return int(key)
  inp = formulas[key]
  print key, inp

  if len(inp) == 1:
    res = solve(inp[0])
  elif len(inp) == 2:
    res = ~solve(inp[1])
  else:
    command = inp[1]
    if command == 'AND':
      res = solve(inp[0]) & solve(inp[2])
    elif command == 'OR':
      res = solve(inp[0]) | solve(inp[2])
    elif command == 'LSHIFT':
      res = solve(inp[0]) << solve(inp[2])
    elif command == 'RSHIFT':
      res = solve(inp[0]) >> solve(inp[2])
  cache[key] = res
  return res

s = solve('a')
cache = {}
cache['b'] = s
print solve('a')
