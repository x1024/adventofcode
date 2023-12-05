import collections
import numpy
import pprint
import re
import functools
import itertools

def play_round(row):
    game, cards = row.split(":")
    have, winning = cards.split("|")
    game = game.replace("Card ", "")
    have = have.split()
    winning = winning.split()
    matches = set(have).intersection(set(winning))
    return int(2**((len(matches)) - 1 ))

def main(data):
    return sum(map(play_round, [row.strip() for row in data.split('\n')]))


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
