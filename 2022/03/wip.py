alphabet = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def priority(group):
  return alphabet.index(''.join(set.intersection(*map(set, group))))


def easy(input):
  groups = [(r[int(len(r) // 2):], r[:int(len(r) // 2)]) for r in input]
  return sum(map(priority, groups))


def hard(input):
  groups = [input[i:i+3] for i in range(0, len(input), 3)]
  return sum(map(priority, groups))


input = open('input.txt', 'r').read().strip().split('\n')
print(easy(input))
print(hard(input))
