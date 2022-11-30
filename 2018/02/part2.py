import pprint
import collections

def solve(input):
  # pprint.pprint(input)
  for x in range(len(input)):
    for y in range(x + 1, len(input)):
      wa = input[x]
      wb = input[y]
      # print(wa, wb)
      diff = 0
      for i in range(len(wa)):
        if wa[i] != wb[i]: diff += 1
      if diff == 1:
        print(wa, wb)
        print(wa)
        print(wb)
        res = []
        for i in range(len(wa)):
          if wa[i] == wb[i]: res.append(wa[i])
        print(''.join(res))
  return 0


def parse_line(input):
  return input


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
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
