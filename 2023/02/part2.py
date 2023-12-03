import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()
data_test = open('input-sample.txt', 'r').read().strip()

# data = data_test

data = data.split('\n')
data = [row.strip() for row in data]
data = [row for row in data if row]
# data = list(map(int, data))
# data = [row.split() for row in data]

given = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

result = 0
for row in data:
    game, d = row.split(": ")
    game = int(game.replace("Game ", ""))
    balls = {}
    for draw in d.split("; "):
        for b in draw.split(", "):
            n, color = b.split(" ")
            balls[color] = max(int(n), balls.get(color, 0))
    # print(game, balls)

    power = balls['red'] * balls['green'] * balls['blue']

    result += power

    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

pprint.pprint(data)
print(result)



print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

import IPython
IPython.embed()
