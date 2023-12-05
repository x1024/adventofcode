import collections
import functools

def play_round(round): return len(functools.reduce(lambda a, b: set(a).intersection(set(b)), [s.split() for s in round.split(":")[1].split("|")]))
winnings = list(map(play_round, open('input.txt', 'r').read().strip().split('\n')))

@functools.lru_cache(maxsize=None)
def num_cards(i): return 1 + sum(num_cards(j) for j in range(i) if j + winnings[j] >= i)

print(sum(int(2**(round - 1)) for round in winnings))
print(sum(map(num_cards, range(len(winnings)))))
