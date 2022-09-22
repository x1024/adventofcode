def check(row, correct):
  for key in correct:
    if key not in row: continue
    if correct[key] != row[key]:
      return False
  return True

def solve(input, correct):
  print input
  for name, row in input.items():
    if check(row, correct):
      print name
  # print input
  return 0


def parse_line(input):
  segments = input.split(": ")
  name = segments[0]
  config = dict([cell.split() for cell in ': '.join(segments[1:]).split(', ')])
  index = name.split()[-1]
  return index, config


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = map(int, input)
  input = map(parse_line, input)
  input = dict(input)
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
correct = 'Sue -1: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, goldfish: 5, trees: 3, cars: 2, perfumes: 1'
_, correct = parse_line(correct)
print correct
result = solve(input, correct)
print("Result: {}".format(result))
