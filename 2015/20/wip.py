def solve(input):
  n = input
  n = 10
  data = sieve(n)
  while max(data) < input:
    print(n, max(data))
    data = sieve(n)
    n = n * 10

  for i in range(len(data)):
    if data[i] >= input:
      return i
  print(input)
  return 0


def parse_line(input):
  return input.split()


def parse_input(input):
  # input = input.split('\n')
  # input = [row.strip() for row in input]
  # input = [row for row in input if row]
  # input = map(int, input)
  # input = map(parse_line, input)
  input = int(input)
  return input


def sieve(n):
  data = [0] * n
  for i in range(1, n):
    d = i
    count = 0
    while i < n and count < 50:
      data[i] += d*11
      i += d
      count += 1
  return data

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
