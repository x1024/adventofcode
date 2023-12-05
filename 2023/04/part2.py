import collections
import numpy
import pprint
import re
import functools
import itertools


def main(data):
    # pprint.pprint(data)
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = list(map(int, data))

    numcards = {}
    res = 0
    for row in data:
        game, cards = row.split(":")
        have, winning = cards.split("|")
        game = int(game.replace("Card ", ""))
        numcards[game] = numcards.get(game, 0) + 1
        current_card = numcards[game]
        have = have.split()
        winning = winning.split()
        matches = set(have).intersection(set(winning))
        print(game, current_card, len(matches))
        for i in range(len(matches)):
            numcards[game + 1 + i] = numcards.get(game + 1 + i, 0) + current_card

    print(numcards)
    res = sum(numcards.values())
    return res


data_test = open('input-sample.txt', 'r').read().strip()
result = main(data_test)
print("Test Result: {}".format(result))

data = open('input.txt', 'r').read().strip()
result = main(data)
print("Real Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
