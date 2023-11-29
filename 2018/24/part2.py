import pprint
import re


class Army(object):
  def __init__(self, line, name):
    super().__init__()
    self.weak = set()
    self.immune = set()
    self.name = name
    nums = map(int, re.findall("\d+", line))
    self.size, self.hp, self.attack, self.initiative = nums
    self.damage = re.findall("(\w+) damage", line)[0]
    self.is_chosen = False

    for s in re.findall("\((.+)\)", line):
      for t in s.split("; "):
        words = t.split(" ")
        status = words[0]
        features = set(' '.join(words[2:]).split(', '))
        # print(status, features)
        if status == 'weak': self.weak = features
        if status == 'immune': self.immune = features
  
  def power(self):
    return self.attack * self.size
  
  def calculate_damage(self, opponent):
    damage = self.power()
    # print(self.name, damage, self.damage, opponent.weak, self.damage in opponent.weak)
    if self.damage in opponent.immune: damage = 0
    if self.damage in opponent.weak: damage *= 2
    return damage

  def do_damage(self, opponent):
    damage = self.calculate_damage(opponent)
    killed = min(opponent.size, damage // opponent.hp)
    # print("%s: deal %s damage, killing %s units" % (self.name, damage, killed))
    opponent.size -= killed

  def target_priority(self):
    return -1 * (self.power() * 1000 + self.initiative)

  def __repr__(self):
    return "<Army: power: %s, side: %s>" % (self.power(), self.name)


def choose_target(army, armies):
  max_damage = 0
  best_opponent = None
  for opp in armies:
    if opp.name == army.name: continue
    if opp.is_chosen: continue
    damage = army.calculate_damage(opp)
    if damage > max_damage:
      max_damage = damage
      best_opponent = opp
    elif damage == max_damage and best_opponent:
      if opp.power() > best_opponent.power():
        best_opponent = opp
      elif opp.power() == best_opponent.power() and opp.initiative > best_opponent.initiative:
        best_opponent = opp
  return best_opponent


def do_round(armies):
  armies = list(sorted(armies, key=lambda army: army.target_priority()))
  targets = {}
  for army in armies: army.is_chosen = False
  for army in armies:
    # print(army)
    target = choose_target(army, armies)
    if target:
      targets[army] = target
      target.is_chosen = True

  armies = list(sorted(armies, key=lambda army: -army.initiative))
  for army in armies:
    if army.power() <= 0: continue
    if army not in targets: continue
    opp = targets[army]
    army.do_damage(opp)
  return [army for army in armies if army.power() > 0]

def check_winner(armies):
  # print(armies)
  while len(set(army.name for army in armies)) > 1:
    old_sum = sum(army.size for army in armies)
    armies = do_round(armies)
    new_sum = sum(army.size for army in armies)
    if new_sum == old_sum: return "none", -1
  return armies[0].name, sum(army.size for army in armies)


def solve(input):
  boost = 0
  while True:
    boost += 1
    print(boost)
    armies = parse_input(input)
    for army in armies:
      if army.name == "us": army.attack += boost
    winner, score = check_winner(armies)
    print(winner, score)
    if winner == 'us':
      return score
      break


def parse_group(group, name):
  return list(map(lambda g: Army(g, name), group.split("\n")[1:]))


def parse_input(input):
  input = input.split('\n\n')
  us = parse_group(input[0], "us")
  them = parse_group(input[1], "them")
  # input = [row.strip() for row in input]
  # input = [row for row in input if row]
  # input = list(map(int, input))
  # input = list(map(parse_line, input))
  return us + them


def test():
  input = '''
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4'''.strip("\n")
  # result = check_winner(parse_input(input))
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
print(check_winner(parse_input(input)))
result = solve(input)
# print("Result: {}".format(result))
