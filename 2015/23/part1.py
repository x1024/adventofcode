def solve(input):
  index = 0
  data = { 'a': 0, 'b': 0 }

  while True:
    if index < 0 or index >= len(input):
      break
    code, tgt, *rest = input[index]
    offset = 1
    if code == 'hlf':
      data[tgt] //= 2
    elif code == 'tpl':
      data[tgt] *= 3
    elif code == 'inc':
      data[tgt] += 1
    elif code == 'jmp':
      offset = int(tgt)
    elif code == 'jie':
      offset = int(rest[0]) if data[tgt] % 2 == 0 else 1
    elif code == 'jio':
      offset = int(rest[0]) if data[tgt] == 1 else 1
    index += offset
    print(code, tgt, rest, index, data)
  print(index, data)
  return data['b']


def parse_line(input):
  return input.split()

def parse_input(input):
  input = input.split('\n')
  input = [row.replace(",", "").strip().split() for row in input]
  input = [row for row in input if row]
  # input = map(int, input)
  # input = map(parse_line, input)
  return input


def test():
  input = '''
   inc a      
jio a, +2  
tpl a      
inc a 
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
