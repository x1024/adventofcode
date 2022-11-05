from operator import eq
from queue import PriorityQueue

SHIELD_STRENGTH = 7
RECHARGE_STRENGTH = 101
POISON_STRENGTH = 3

PLAYER_WINS = 1
ENEMY_WINS = -1
CONTINUE_BATTLE = 0

class Character(object):
  def __init__(self, hp, mana, damage):
    self.hp = hp
    self.mana = mana
    self.damage = damage
    self.armor = 0
    self.effects = []

  def copy(self):
    c = Character(self.hp, self.mana, self.damage)
    c.effects = list(self.effects)
    return c

  def __lt__(self, other):
    d = self.hp - other.hp
    if d != 0: return d
    d = self.hp - other.mana
    if d != 0: return d
    d = self.hp - other.damage
    return d

  def __str__(self):
    return "(%s %s %s %s)" % (self.hp, self.mana, self.damage, self.effects)

  def has_effect(self, effect):
    return len([e for e in self.effects if e[0] == effect]) > 0

  def add_effect(self, effect, duration):
    self.effects.append((effect, duration))

  def effects_timeout(self):
    self.effects = [(a, b - 1) for (a, b) in self.effects]
    self.effects = [e for e in self.effects if e[1] > 0]


def magic_missile(player, boss):
  cost = 53
  if player.mana < cost:
    return False, 0
  player.mana -= cost
  boss.hp -= 4
  return True, cost

def drain(player, boss):
  cost = 73
  if player.mana < cost:
    return False, 0
  player.mana -= cost
  player.hp += 2
  boss.hp -= 2
  return True, cost

def shield(player, boss):
  if player.has_effect('shield'):
    return False, 0
  cost = 113
  if player.mana < cost:
    return False, 0
  player.mana -= cost
  player.add_effect('shield', 6)
  player.effects
  return True, cost

def poison(player, boss):
  if boss.has_effect('poison'):
    return False, 0
  cost = 173
  if player.mana < cost:
    return False, 0
  player.mana -= cost
  boss.add_effect('poison', 6)
  return True, cost

def recharge(player, boss):
  if player.has_effect('recharge'):
    return False, 0
  cost = 229
  if player.mana < cost:
    return False, 0
  player.mana -= cost
  player.add_effect('recharge', 5)
  return True, cost

spells = [
  magic_missile, drain, shield, poison, recharge
]


def battle(c_a, c_b, spell):
  # print("BATTLE")
  # print (c_a, c_b)
  # player turn
  if c_a.has_effect('recharge'):
    c_a.mana += RECHARGE_STRENGTH
  if c_b.has_effect('poison'):
    c_b.hp -= POISON_STRENGTH

  c_a.effects_timeout()
  c_b.effects_timeout()

  if c_b.hp <= 0: return PLAYER_WINS, 0
  result, cost = spell(c_a, c_b)
  # print("Casting %s %s %s" % (spell, result, cost))
  # print ("player's turn over:", c_a, c_b)

  if not result:
    return ENEMY_WINS, 0
  if c_b.hp <= 0: return PLAYER_WINS, cost

  # boss turn
  if c_a.has_effect('recharge'):
    c_a.mana += RECHARGE_STRENGTH
  if c_b.has_effect('poison'):
    c_b.hp -= POISON_STRENGTH
  dmg = c_b.damage
  if c_a.has_effect('shield'):
    dmg = max(1, dmg - SHIELD_STRENGTH)
  c_a.hp -= dmg

  c_a.effects_timeout()
  c_b.effects_timeout()

  # print ("boss's turn over:", c_a, c_b)
  if c_b.hp <= 0: return PLAYER_WINS, cost
  if c_a.hp <= 0: return ENEMY_WINS, 0
  return CONTINUE_BATTLE, cost


def solve(enemy):
  best_score = 9999999999
  hero = Character(50, 500, 0)
  enemy = Character(enemy[0], 0, enemy[1])
  print(hero, enemy)

  # hero = Character(10, 250, 0)
  # enemy = Character(14, 0, 8)

  q = PriorityQueue()
  q.put((0, hero, enemy))
  # print(hero, enemy)

  while not q.empty():
    mana_spent, hero, enemy = q.get()
    if mana_spent >= best_score:
      continue
    print(mana_spent, best_score, hero, enemy, q.qsize())
    for spell in spells:
      h = hero.copy()
      e = enemy.copy()
      res, cost = battle(h, e, spell)
      new_mana_spent = mana_spent + cost
      if res == ENEMY_WINS:
        continue
      if res == PLAYER_WINS:
        best_score = min(best_score, new_mana_spent)
      q.put((new_mana_spent, h, e))
  

  print("!!!!!!!!!!!!!")
  print(best_score)
  print("!!!!!!!!!!!!!")
  return best_score


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  input = [int(row.split(':')[1]) for row in input]
  # input = map(int, input)
  # input = map(parse_line, input)
  input = tuple(input)
  return input


def test():
  input = '''
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
