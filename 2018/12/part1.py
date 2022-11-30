import pprint
import collections
import numpy

def step(state, rules):
  newstate = collections.defaultdict(lambda: 0)
  keys = list(state.keys())
  for x in range(min(keys) - 4, max(keys) + 5):
    key = (state[x-2], state[x-1], state[x], state[x+1], state[x+2])
    newstate[x] = rules[key]
  return newstate


def solve(state, rules):
  for i in range(20):
    state = step(state, rules)
    print(i, len(state))
    # print(''.join(map(o, [state[i] for i in range(-5, 40)])))
  res = sum(k for k,v in state.items() if v > 0)
  return res

def o(i):
  return '#' if i == 1 else '.'

def c(char):
  return 1 if char == '#' else 0

def parse_line(input):
  return [tuple(map(c, cell)) for cell in input.split(' => ')]


def parse_input(input):
  input = input.split('\n')
  state = input[0].replace('initial state: ', '')
  initial = collections.defaultdict(lambda: 0)
  initial.update(tuple(enumerate(map(c, state))))
  rules = input[2:]
  rules = [row.strip() for row in rules]
  rules = [row for row in rules if row]
  # rules = list(map(int, rules))
  rulesDict = collections.defaultdict(lambda: 0)
  rulesDict.update((k, v[0]) for k, v in map(parse_line, rules))
  return initial, rulesDict



def test():
  input = '''initial state: #..#.#..##......###...###

...## => #                              
..#.. => #                              
.#... => #                              
.#.#. => #                              
.#.## => #                              
.##.. => #                              
.#### => #                              
#.#.# => #                              
#.### => #                              
##.#. => #                              
##.## => #                              
###.. => #                              
###.# => #                              
####. => #        '''
  input = parse_input(input)
  result = solve(*input)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(*input)
print("Result: {}".format(result))
