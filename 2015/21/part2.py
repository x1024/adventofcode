from operator import eq


weapons = [
  ['Dagger', 8, 4, 0],
  ['Shortsword', 10, 5, 0],
  ['Warhammer', 25, 6, 0],
  ['Longsword', 40, 7, 0],
  ['Greataxe', 74, 8, 0],
]

armors = [
  ['Nothing', 0, 0, 0],
  ['Leather', 13, 0, 1],
  ['Chainmail', 31, 0, 2],
  ['Splintmail', 53, 0, 3],
  ['Bandedmail', 75, 0, 4],
  ['Platemail', 102, 0, 5],
]

rings = [
  ['Nothing 1', 0, 0, 0],
  ['Nothing 2', 0, 0, 0],
  ['Damage + 1', 25, 1, 0], 
  ['Damage + 2', 50, 2, 0], 
  ['Damage + 3', 100, 3, 0], 
  ['Defense + 1', 20, 0, 1], 
  ['Defense + 2', 40, 0, 2], 
  ['Defense + 3', 80, 0, 3],
]

def fight(char_a, char_b):
  hp0, dmg0, arm0 = list(char_a)
  hp1, dmg1, arm1 = list(char_b)
  while True:
    hp1 -= max(1, dmg0 - arm1)
    if hp1 <= 0: return True
    hp0 -= max(1, dmg1 - arm0)
    if hp0 <= 0: return False


def solve(enemy):
  max_cost = 0
  for weapon in weapons:
    for armor in armors:
      for r1 in range(0, len(rings)):
        for r2 in range(r1 + 1, len(rings)):
          ring1 = rings[r1]
          ring2 = rings[r2]
          equip = [weapon, armor, ring1, ring2]
          
          cost = sum(e[1] for e in equip)
          dmg = sum(e[2] for e in equip)
          arm = sum(e[3] for e in equip)
          hp = 100
          hero = (hp, dmg, arm)
          if not fight(hero, enemy) and cost > max_cost:
            max_cost = cost
  return max_cost


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
