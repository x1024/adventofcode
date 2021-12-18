#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import itertools

def solve(line, time_left):
    (name, speed, duration, rest) = line

    total_distance = 0
    while time_left >= 0:
        time_travelled = min(duration, time_left)
        total_distance += time_travelled * speed
        time_left -= time_travelled
        time_left -= rest
    return (total_distance, name)


def easy(data, limit = 100, calorie_limit = None):
    data = [line.strip() for line in data.split("\n")]
    data = [line for line in data if line]
    lines = map(parse_line, data)

    choice = []

    def score(choice):
        score1 = max(0, sum(number * line[1] for number, line in zip(choice, lines)))
        score2 = max(0, sum(number * line[2] for number, line in zip(choice, lines)))
        score3 = max(0, sum(number * line[3] for number, line in zip(choice, lines)))
        score4 = max(0, sum(number * line[4] for number, line in zip(choice, lines)))

        if calorie_limit:
            calories = sum(number * line[5] for number, line in zip(choice, lines))
            if calories != calorie_limit:
                return -1

        total_score = score1 * score2 * score3 * score4
        # print choice, total_score
        return total_score

    def solve(index, limit):
        if index == len(data) - 1:
            choice.append(limit)
            current_score = score(choice)
            choice.pop()
            return current_score

        max_score = 0
        for i in range(0, limit + 1):
            choice.append(i)
            max_score = max(max_score, solve(index + 1, limit - i))
            choice.pop()
        # print max_score
        return max_score

    max_score = solve(0, limit)
    return max_score


def hard(data):
    return easy(data, calorie_limit = 500)


def parse_line(line):
    words = line.split(' ')
    name = words[0].strip(':')
    capacity = int(words[2].strip(','))
    durability = int(words[4].strip(','))
    flavor = int(words[6].strip(','))
    texture = int(words[8].strip(','))
    calories = int(words[10].strip(','))
    return (name, capacity, durability, flavor, texture, calories)


def test():
    assert parse_line('Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8') == ('Butterscotch', -1, -2, 6, 3, 8)
    data = '''
        Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
        Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
    '''
    assert easy(data) == 62842880
    assert hard(data) == 57600000



test()
data = '\n'.join(list(sys.stdin))
print easy(data)
print hard(data)
