def parse_line(line):
  # Frosting: capacity 4, durability -2, flavor 0, texture 0, calories 5
  data = {}
  ingredient, definition = line.split(":")
  for key in definition.split(','):
    name, quantity = key.split()
    data[name] = int(quantity)
  # return (ingredient, data)
  del data['calories']
  return data

def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  input = map(parse_line, input)
  # input = map(int, input)
  return input

def use(ingredient, count):
  data = {}
  for key, value in ingredient.items():
    data[key] = value * count
  return data

def combine(ingredients):
  data = {}
  for key in ingredients[0]:
    data[key] = sum(ingredient[key] for ingredient in ingredients)
  return data

def get_score(data):
  total = 1
  for key in data:
    total *= max(0, data[key])
  return total

def solve2(left = 4, total = 100):
  if left == 1:
    yield (total, )
    return
  for used in range(total + 1):
    for s in solve2(left - 1, total - used):
      yield (used, ) + s

def solve(input, total = 100):
  if len(input) == 1:
    # print len(input), total, get_score(use(input[0], total))
    return use(input[0], total)
  
  l = len(input)
  combinations = solve2(l)
  best = 0
  for c in combinations:
    total = [use(input[i], c[i]) for i in range(l)]
    current = combine(total)
    score = get_score(current)
    if score > best:
      best = score
      solution = current
  return solution


input = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
# for row in input: print row
# print '-----'
# exit()
result = solve(input)
result = get_score(result)
print("Result: {}".format(result))
