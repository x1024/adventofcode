import collections
import numpy
import pprint
import re
import functools
import itertools
import math

'''
Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
'''

def hand_value(hand):
    hand = sorted(hand, key=lambda x: x[0])
    hand = [card[0] for card in hand]
    hand = ''.join(hand)
    collect = collections.Counter(hand)
    v = sorted(collect.values())[::-1]
    # print(hand, v)
    if v == [5]:
        return 0 # five of a kind
    if v == [4, 1]:
        return 1 # four of a kind
    if v == [3, 2]:
        return 2 # full house
    if v == [3, 1, 1]:
        return 3 # three of a kind
    if v == [2, 2, 1]:
        return 4 # two pair
    if v == [2, 1, 1, 1]:
        return 5
    return 6

card_values = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
    'J': 1,
}

def hand_numbers(hand):
    # hand = sorted(hand, key=lambda x: x[0])
    hand = [card[0] for card in hand]
    hand = ''.join(hand)
    return [-1 * card_values[card] for card in hand]


# print(hand_numbers('T55J5'))
# print(hand_numbers('555JA'))
# print(hand_numbers('T55J5') < hand_numbers('555JA'))
# exit()


def hand_variations(hand):
    # print(hand)
    if len(hand) == 0:
        yield ''
        return

    rest = list(hand_variations(hand[1:]))
    c = hand[0]
    if c == 'J':
        vars = 'A K Q J T 9 8 7 6 5 4 3 2'.split()
    else:
        vars = [c]
    for i in vars:
        # print(i, rest, len(rest))
        for r in rest:
            yield i + r


def hand_strength(hand):
    h = sorted(hand_variations(hand), key=lambda x: hand_value(x))[::]
    h = h[0]
    # print(h)
    return hand_value(h), hand_numbers(hand)


def compare_hands(hand1, hand2):
    pass


# print(hand_numbers('JJJJJ'))
# print(hand_numbers('AAAAA'))
# print(hand_strength('JJJJJ'))
# print(hand_strength('QJJQQ') > hand_strength('AAAAA'))
# exit()

def main(data):
    # pprint.pprint(data)
    data = [row.strip() for row in data.split("\n")]
    data = [row for row in data if row]
    # data = [row.split() for row in data]
    # data = list(map(int, data))
    data = [row.split() for row in data]
    # data = [(''.join(sorted(a)), b) for a, b in data]
    data = sorted(data, key=lambda x: hand_strength(x[0]))[::-1]

    result = 0
    for i, row in enumerate(data):
        hand, bid = row
        print(hand, bid, hand_strength(hand))
        # print(bid, i + 1, int(bid) * (i + 1))
        result += int(bid) * (i + 1)

    print(result)
    return result


print(main(open('input-sample.txt', 'r').read().strip()))
# 5905.

result = 0
result = main(open('input.txt', 'r').read().strip())
print(result)

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
