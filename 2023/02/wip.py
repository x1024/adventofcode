import collections
import functools
import numpy
import pprint
import re

# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
def parse_row(row):
    game, d = row.split(": ")
    game = int(game.replace("Game ", ""))
    balls = {}
    for draw in d.split("; "):
        for b in draw.split(", "):
            n, color = b.split(" ")
            balls[color] = max(int(n), balls.get(color, 0))
    return game, balls


data = open('input.txt', 'r').read().strip()
data_test = open('input-sample.txt', 'r').read().strip()
# data = data_test
data = [row.strip() for row in data.split('\n')]
data = [parse_row(row) for row in data]

limit = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

part_a = sum(game
    for game, balls in data
    if sum(balls[key] <= limit[key] for key in balls.keys()) == len(balls))

print("part_a: {}".format(part_a))

part_b = sum(functools.reduce(lambda a, b: a*b, balls.values(), 1)
    for game, balls in data)
print("part_b: {}".format(part_b))
