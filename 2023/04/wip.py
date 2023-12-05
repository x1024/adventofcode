import functools

def play_round(row): return len(functools.reduce(lambda a, b: set(a).intersection(set(b)), [s.split() for s in row.split(":")[1].split("|")]))

data = open('input.txt', 'r').read().strip().split('\n')
print(sum(int(2**(play_round(row) - 1)) for row in data))
print(sum(functools.reduce(lambda cards, row:
                            dict((i, cards[i] + (cards[row[0]] if row[0] + 1 <= i < row[0] + 1 + play_round(row[1]) else 0))
                                 for i in cards),
                           enumerate(data), dict((game, 1) for game in range(len(data)))).values()))
