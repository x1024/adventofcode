import IPython
import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()
data_test = '''
Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian.
'''
ore, clay, obsidian, geode = [1, 0, 0, 0]
# data = data_test

LIMIT = 20
MOD = 100

def clamp(value, limit):
  value = decode(value)
  value = [min(limit[i], value[i]) for i in range(4)]
  value = encode(value)
  return value

def encode(tpl):
  res = min(LIMIT, tpl[0])
  res *= MOD
  res += min(LIMIT, tpl[1])
  res *= MOD
  res += min(LIMIT, tpl[2])
  res *= MOD
  res += min(LIMIT, tpl[3])
  return res

def decode(tpl):
  res = []
  res.append(tpl % MOD)
  tpl //= MOD
  res.append(tpl % MOD)
  tpl //= MOD
  res.append(tpl % MOD)
  tpl //= MOD
  res.append(tpl % MOD)
  tpl //= MOD
  return res[::-1]

def parse_row(row):
  a = list(map(int, re.findall("\d+", row)))
  index = a[0]
  res = [
    # how much to pay -> what you're getting
    (encode([0, 0, 0, 0]), encode((0, 0, 0, 0))),
    (encode([a[1], 0, 0, 0]), encode((1, 0, 0, 0))),
    (encode([a[2], 0, 0, 0]), encode((0, 1, 0, 0))),
    (encode([a[3], a[4], 0, 0]), encode((0, 0, 1, 0))),
    (encode([a[5], 0, a[6], 0]), encode((0, 0, 0, 1))),
  ][::-1]
  return index, res

data = data.strip('\n').split('\n')
data = [row.split('\n')[0] for row in data]
data = [parse_row(row) for row in data if row]

def solve(prices):
  cash_limits = []
  robot_limits = []
  for i in range(4):
    limit = max(decode(price)[i] for price, robots in prices)
    cash_limits.append(50)
    robot_limits.append(limit + 1)
  cash_limits[-1] = 100
  robot_limits[-1] = 100
  print(cash_limits)
  print(robot_limits)

  def can_pay(cash, price):
    if cash % MOD < price % MOD: return False
    cash //= MOD
    price //= MOD
    if cash % MOD < price % MOD: return False
    cash //= MOD
    price //= MOD
    if cash % MOD < price % MOD: return False
    cash //= MOD
    price //= MOD
    if cash % MOD < price % MOD: return False
    return True

  memo = {}
  rng = [3, 2, 1, 0]
  best = [0]
  def rec(state):
    if state not in memo:
      res = 0
      minutes, cash, robots = state
      if minutes == 0:
        res = cash % MOD
      else:
        # options:
        for price, robots_built in prices:
          if not can_pay(cash, price): continue
          new_cash = cash + robots - price
          # new_cash = clamp(new_cash, cash_limits)
          new_robots = robots + robots_built
          new_robots = clamp(new_robots, robot_limits)
          # if not can_pay(max_robots, new_robots): continue
          new_state = (minutes - 1, new_cash, new_robots)
          if len(memo) % 100000 == 1:
            print("\t\t", 24 - new_state[0], decode(new_state[1]), decode(new_state[2]), len(memo), max(memo.values()))
          res = max(res, rec(new_state))
          best[0] = max(best[0], res)

      memo[state] = res
    return memo[state]

  minutes = 24
  cash = encode((0, 0, 0, 0))
  robots = encode((1, 0, 0, 0))
  state = (minutes, cash, robots)
  result = rec(state)
  print(result)
  return result

result = 0
f = open("tmp.txt", "w")
for index, blueprint in data:
  geodes = solve(blueprint)
  quality = index * geodes
  result += quality
  print(result, geodes, index, quality, blueprint)
  f.write("%d %d %d\n" % (index, geodes, quality))
  f.flush()


print(result)



print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
