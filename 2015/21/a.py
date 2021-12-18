#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import re
import queue

# cost, damage, armor = item

weapons = [
    [8, 4, 0],
    [10, 5, 0],
    [25, 6, 0],
    [40, 7, 0],
    [74, 8, 0],
]

armours = [
    [13, 0, 1],
    [31, 0, 2],
    [53, 0, 3],
    [75, 0, 4],
    [102, 0, 5],
]

rings = [
    [25, 1, 0],
    [50, 2, 0],
    [100, 3, 0],
    [20, 0, 1],
    [40, 0, 2],
    [80, 0, 3],
]


def battle(player, boss):
    player = list(player)
    boss = list(boss)
    HP = 0
    DAMAGE = 1
    ARMOR = 2
    # print 'battle', player, boss
    while True:
        player_damage = max(1, player[DAMAGE] - boss[ARMOR])
        # print player_damage, boss[HP], boss[HP] - player_damage
        boss[HP] -= player_damage
        if boss[HP] <= 0:
            return True

        boss_damage = max(1, boss[DAMAGE] - player[ARMOR])
        player[HP] -= boss_damage
        # print boss_damage, player[HP], player[HP] - boss_damage
        if player[HP] <= 0:
            return False


def make_player(items):
    hp = 100
    cost = sum(item[0] for item in items)
    attack = sum(item[1] for item in items)
    defense = sum(item[2] for item in items)
    # print ( hp, attack, defense ), cost
    return ( hp, attack, defense ), cost


def easy(boss, expected_result = True, aggregation = min):
    costs = []
    for weapon in weapons:
        items = [weapon]
        player, cost = make_player(items)
        if battle(player, boss) == expected_result:
            costs.append((cost, items))
        for armor in armours:
            items = [weapon, armor]
            player, cost = make_player(items)
            if battle(player, boss) == expected_result:
                costs.append((cost, items))
            for ring1 in rings:
                items = [weapon, armor, ring1]
                player, cost = make_player(items)
                if battle(player, boss) == expected_result:
                    costs.append((cost, items))
                for ring2 in rings:
                    if ring1 == ring2:
                        continue
                    items = [weapon, armor, ring1, ring2]
                    player, cost = make_player(items)
                    if battle(player, boss) == expected_result:
                        costs.append((cost, items))

                    items = [weapon, ring1, ring2]
                    player, cost = make_player(items)
                    if battle(player, boss) == expected_result:
                        costs.append((cost, items))
    return aggregation(costs)[0]


def hard(boss):
    return easy(boss, False, max)


def test():
    assert make_player([( 10, 0, 0 )]) == (( 100, 0, 0 ), 10)


test()

# hp, attack, defense
stats = [109, 8, 2]
print easy(stats)
print hard(stats)
