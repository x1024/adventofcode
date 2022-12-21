import re


# encoding coordinates is very pointless, but I love it anyway
def encode(tpl):
  return (tpl[0] << 16) | (tpl[1] << 8) | (tpl[2])


def decode(code):
  # 255 << 8 == 65280
  # 255 << 16 == 16711680
  return ((code & 16711680) >> 16, (code & 65280) >> 8, (code & 255))


def clamp(a, b):
  return (
    min((a & 16711680), (b & 16711680)) |
    min((a & 65280), (b & 65280)) |
    min((a & 255), (b & 255))
  )


def gte(a, b):
  return (
    (a & 16711680) >= (b & 16711680) and
    (a & 65280) >= (b & 65280) and
    (a & 255) >= (b & 255)
  )


def parse_blueprint(row):
  a = list(map(int, re.findall("\d+", row)))
  index = a[0]
  res = [
    # how much to pay | what you're getting | how many geodes you're getting
    # note that there's nothing that can be purchased with geodes
    # note that only 1 of anything can be purchased at once
    # (including geodes, which is very important)
    ((   0, 0,    0), (0, 0, 0), 0), # this is the "builds nothing" state
    ((a[1], 0,    0), (1, 0, 0), 0),
    ((a[2], 0,    0), (0, 1, 0), 0),
    ((a[3], a[4], 0), (0, 0, 1), 0),
    ((a[5], 0, a[6]), (0, 0, 0), 1),
  ]
  return index, res


def solve(prices, max_minutes=24):
  # Note: I "encode" all lists into a single integer
  # "because it's technically faster to add 2 things together that way",
  # and because it's faster to hash an integer than a list of 4integers
  # This has no further meaning, and it might not even be faster, honestly

  cash_limits = []
  robot_limits = []
  for i in range(3):
    limit = max(price[i] for price, robots, geodes in prices)
    cash_limits.append(limit * 2) # This is arbitrary, and discovered empirically
    robot_limits.append(limit)

  prices = [(encode(price), encode(robots), geodes) for price, robots, geodes in prices]
  # no point in going over the limits
  # At no point does it ever make sense to have more than X robots of a given type
  # Where X is the highest cost of anything that can be purchased
  robot_limits = encode(robot_limits)

  # it's never necessary to have more than a certain amount of cash
  # therefore, having 10000 ore and 100 ore results in exactly the same result
  # (In all practical cases. Obviously if you only have 1 ore bot, a new bot costs 100, and SOMEHOW have 10000 ore,
  # that's a different situation than if you only have 1 ore bot, a new bot costs 100, and only have 1 ore)
  # But in the given input, these limits can safely be enforced
  cash_limits = encode(cash_limits)

  memo = {}
  best = [0] * (max_minutes + 1)
  def rec(state):
    if state not in memo:
      res = 0
      minutes, cash, robots = (state >> 48) & ~(-1<<24), (state >> 24) & ~(-1<<24), state & ~(-1<<24)
      if minutes == 0:
        res = 0
      else:
        minutes_remaining = minutes - 1
        theoretical_max_geodes = minutes_remaining * (minutes_remaining - 1) // 2
        # options:
        for price, robots_built, geode_robots in prices:
          if theoretical_max_geodes < best[minutes_remaining]: break # can't possibly beat the best score
          if not gte(cash, price): continue # can't pay for it
          new_cash = cash + robots - price # encoding the coordinates allows us to do this
          # note that we're not "pruning" runs with too much cash
          # we're just limiting the cash, because at this point it might as well be "infinite"
          # This makes other "infinite" cash states hit the same... cache... state
          new_cash = clamp(new_cash, cash_limits)
          new_robots = robots + robots_built
          if not gte(robot_limits, new_robots): continue

          new_state = minutes_remaining << 48 | new_cash << 24 | new_robots
          # new_state = (minutes_remaining, new_cash, new_robots)
          # if len(memo) % 100000 == 1: print("\t\t", max_minutes - new_state[0], decode(new_state[1]), decode(new_state[2]), len(memo), max(memo.values()))
          res = max(res, rec(new_state) + geode_robots * minutes_remaining)
        best[minutes] = max(best[minutes], res)

      memo[state] = res
    return memo[state]

  # encode the state's components, so they become a single integer
  cash = encode((0, 0, 0))
  robots = encode((1, 0, 0))
  # yes, we encode the entire state, too. Double-encoding, wadup
  return rec(max_minutes << 48 | cash << 24 | robots)


def easy(data):
  result = 0
  for index, blueprint in data:
    geodes = solve(blueprint, 24)
    quality = index * geodes
    result += quality
    print(index, geodes, quality, result)
    # print(result, geodes, index, quality, blueprint)
  return result


def hard(data):
  result = 1
  data = data[:3]
  for index, blueprint in data:
    geodes = solve(blueprint, 32)
    quality = geodes
    result *= quality
    print(index, geodes, result)
  return result


data = open('input.txt', 'r').read().strip().split("\n")
data = [row.split('\n')[0] for row in data]
data = [parse_blueprint(row) for row in data if row]
print(easy(data))
print(hard(data))