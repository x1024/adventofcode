def next_code(code=20151125, mul=252533, mod=33554393):
  while True:
    return (code * mul) % mod

def solve(input, code = 20151125):
  print(input)
  row, col = input
  print(input)
  x = 1
  y = 1
  while True:
    print(x)
    d = x
    while x >= 1:
      if x == row and y == col:
        print(x, row, col, code)
        return code
      x -= 1
      y += 1
      code = next_code(code)
    x = d + 1
    y = 1
  return 0


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.replace(",","").replace(".","").split()
  input = [int(i) for i in input if i.isnumeric()]
  return input


def test():
  input = '''
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
