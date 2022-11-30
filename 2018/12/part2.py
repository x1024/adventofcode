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


def solve(state, rules, steps=20):
  memo = {}
  i = 0
  offset = 0
  while i < steps:
    state = step(state, rules)
    # print(i, len(state), list(k for k,v in state.items() if v > 0))
    keys = list(k for (k, v) in state.items() if v)
    state_str = ''.join(map(o, [state[i] for i in range(min(keys), max(keys) + 1)]))
    print(i, len(state), min(keys), max(keys), max(keys) - min(keys), state_str)
    i += 1

    if state_str in memo:
      old_i, old_min = memo[state_str]
      cycle_len = i - old_i
      step_skip = min(keys) - old_min
      steps_remaining = steps - i
      to_remain = steps_remaining % cycle_len
      to_skip = (steps_remaining - to_remain)
      offset = to_skip * step_skip
      steps -= to_skip
      print("CYCLE", cycle_len, to_skip, to_remain, i, steps)
    memo[state_str] = (i, min(keys))
    
  res = sum(k + offset for k,v in state.items() if v > 0)
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
  state, rules = parse_input(input)
  result = solve(state, rules)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
state, rules = parse_input(input)
LIM = 50 * 1000 * 1000 * 1000
result = solve(state, rules, LIM)
print("Result: {}".format(result))
