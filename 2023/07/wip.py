import collections

hand_type = lambda hand: tuple(collections.Counter(hand).values())
high_card = lambda hand, card_strength='asdasdas': tuple(card_strength.index(card) for card in hand)
best_variation = lambda hand: sorted(hand.replace('J', card) for card in '23456789TJQKA', key=lambda x: hand_type(x))[-1]
score = lambda data: sum(int(bid) * (i + 1) for i, (hand, bid) in enumerate(data))

data = [row.split() for row in open('input.txt', 'r').read().strip().split("\n")]
print(score(sorted(data, key=lambda hand: (hand_type(hand[0]), high_card(hand[0], '23456789TJQKA')))))
print(score(sorted(data, key=lambda hand: (hand_type(best_variation(hand[0])), high_card(hand[0], 'J23456789TQKA')))))
