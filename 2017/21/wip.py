import numpy


def parse_cell(cell):
  return [list(map(int, row.replace('.', '0').replace('#', '1')))
    for row in cell.split("/")]


def parse_line(input, rules):
  rule, result = input.split(" => ")
  rule = parse_cell(rule)
  result = parse_cell(result)
  rule = numpy.array(rule)
  result = numpy.array(result)

  res = []
  res.append(rule)
  rule = numpy.rot90(rule)
  res.append(rule)
  rule = numpy.rot90(rule)
  res.append(rule)
  rule = numpy.rot90(rule)
  res.append(rule)

  rule = numpy.flipud(rule)
  res.append(rule)
  rule = numpy.rot90(rule)
  res.append(rule)
  rule = numpy.rot90(rule)
  res.append(rule)
  rule = numpy.rot90(rule)
  res.append(rule)

  res = list(set(tuple(rule.flatten()) for rule in res))
  for rule in res:
    rules[rule] = result


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  rules = {}
  for row in input:
    parse_line(row, rules)
  return rules


# https://stackoverflow.com/questions/11105375/how-to-split-a-matrix-into-4-blocks-using-numpy
def split(array, nrows, ncols):
    """Split a matrix into sub-matrices."""

    r, h = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols))

def expand(table, rules, size):
  l = len(table) * (size + 1) // (size)
  data = [[0] * l for _ in range(l)]
  for x in range(len(table) // size):
    for y in range(len(table[0]) // size):
      cell = table[x*size:(x+1)*size, y*size:(y+1)*size]
      cell = tuple(cell.flatten())
      cell = rules[cell]
      for i in range(size + 1):
        for j in range(size + 1):
          data[x*(size+1) + i][y*(size+1) + j] = cell[i][j]
  data = numpy.array(data)
  return data


def process(table, rules, steps = 2):
  # print(table)
  while steps > 0:
    print(steps, len(table))
    steps -= 1
    if len(table) % 2 == 0:
      table = expand(table, rules, 2)
    else:
      table = expand(table, rules, 3)
    # print(table)
  table = table.flatten()
  return sum(table)


def test():
  input = '''
  ../.# => ##./#../...
  .#./..#/### => #..#/..../..../#..#
'''
  rules = parse_input(input)
  start = parse_cell('''.#./..#/###''')
  start = numpy.array(start)
  result = process(start, rules, 2)
  assert result == 12


# test()
input = open('input.txt', 'r').read().strip()
rules = parse_input(input)
start = numpy.array(parse_cell('''.#./..#/###'''))
result = process(start, rules, 18)
print("Result: {}".format(result))
