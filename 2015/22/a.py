#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import queue

# name, cost, duration, damage, heal, armor, mana
spells = [
    ('Magic Missile', 53, 1, 4, 0, 0, 0),
    ('Drain', 73, 1, 2, 2, 0, 0),
    ('Shield', 113, 6, 0, 0, 7, 0),
    ('Poison', 173, 6, 3, 0, 0, 0),
    ('Recharge', 229, 5, 0, 0, 0, 101),
]


def easy_manual(hp, mana, boss_hp, boss_damage):
    q = queue.LifoQueue()
    PLAYER_TURN = 1
    BOSS_TURN = 0
    q.put((0, hp, mana, boss_hp, 0, [], []))

    wins = []

    while not q.empty():
        row = q.get()
        (turn, hp, mana, boss_hp, spent, effects, story) = row
        if hp <= 0:
            print "DEAD"
            continue
        if mana <= 0:
            print "DEAD"
            continue
        armor = 0
        effect_names = [effect for effect, _ in effects]
        if 'Magic Missile' in effect_names:
            print "MISSILE"
            boss_hp -= 4
        if 'Drain' in effect_names:
            hp += 2
            boss_hp -= 2
        if 'Shield' in effect_names:
            armor = 7
        if 'Poison' in effect_names:
            boss_hp -= 3
        if 'Recharge' in effect_names:
            mana += 101

        effects = [(effect, duration - 1) for effect, duration in effects]
        effects = [(effect, duration) for effect, duration in effects if duration > 0]
        effect_names = [effect for effect, _ in effects]

        if boss_hp <= 0:
            print "WIN"
            print (spent, turn)
            wins.append((spent, turn, story))
            continue

        if turn % 2 == 0:
            # player turn
            while True:
                print (turn, hp, mana, boss_hp, spent, effects, story)
                i = int(raw_input('Choose spell: '))
                if i == 1 and 'Magic Missile' not in effect_names:
                    spell = 'Magic Missile'
                    q.put((turn + 1, hp, mana - 53, boss_hp, spent + 53,
                        effects + [(spell, 1)],
                        story + [spell],
                    ))
                    break
                elif i == 2 and 'Drain' not in effect_names:
                    spell = 'Drain'
                    q.put((turn + 1, hp, mana - 73, boss_hp, spent + 73,
                        effects + [(spell, 1)],
                        story + [spell],
                    ))
                    break
                elif i == 3 and 'Shield' not in effect_names:
                    spell = 'Shield'
                    q.put((turn + 1, hp, mana - 113, boss_hp, spent + 113,
                        effects + [(spell, 6)],
                        story + [spell],
                    ))
                    break
                elif i == 4 and 'Poison' not in effect_names:
                    spell = 'Poison'
                    q.put((turn + 1, hp, mana - 173, boss_hp, spent + 173,
                        effects + [(spell, 6)],
                        story + [spell],
                    ))
                    break
                elif i == 5 and 'Recharge' not in effect_names:
                    spell = 'Recharge'
                    q.put((turn + 1, hp, mana - 279, boss_hp, spent + 229,
                        effects + [(spell, 5)],
                        story + [spell],
                    ))
                    break
                print "INVALID SPELL"
            
        else:
            # boss turn
            hp -= max(1, boss_damage - armor)
            if hp <= 0:
                print "DEAD"
                continue
            if mana <= 0:
                print "CAN'T CAST"
                continue
            q.put((turn + 1, hp, mana, boss_hp, spent, effects, story))

        if hp <= 0:
            continue

    print wins


def solve(hp, mana, boss_hp, boss_damage, is_hard=False):
    q = queue.Queue()
    PLAYER_TURN = 1
    BOSS_TURN = 0
    q.put((0, hp, mana, boss_hp, 0, [], []))

    wins = []
    best = 99999999999

    while not q.empty():
        row = q.get()
        (turn, hp, mana, boss_hp, spent, effects, story) = row
        if best < spent: continue
        if hp <= 0: continue
        if mana <= 0: continue

        if is_hard and turn % 2 == 0:
            # player turn
            hp -= 1
            if hp <= 0: continue

        armor = 0
        effect_names = [effect for effect, _ in effects]
        if 'Magic Missile' in effect_names:
            boss_hp -= 4
        if 'Drain' in effect_names:
            hp += 2
            boss_hp -= 2
        if 'Shield' in effect_names:
            armor = 7
        if 'Poison' in effect_names:
            boss_hp -= 3
        if 'Recharge' in effect_names:
            mana += 101

        effects = [(effect, duration - 1) for effect, duration in effects]
        effects = [(effect, duration) for effect, duration in effects if duration > 0]
        effect_names = [effect for effect, _ in effects]

        if boss_hp <= 0:
            best = min(best, spent)
            wins.append((spent, turn, story))
            continue

        if turn % 2 == 0:
            # player turn
            # print (turn, hp, mana, boss_hp, spent, effects, story)
            if 'Magic Missile' not in effect_names:
                spell = 'Magic Missile'
                q.put((turn + 1, hp, mana - 53, boss_hp, spent + 53,
                    effects + [(spell, 1)],
                    story + [spell],
                ))
            if 'Drain' not in effect_names:
                spell = 'Drain'
                q.put((turn + 1, hp, mana - 73, boss_hp, spent + 73,
                    effects + [(spell, 1)],
                    story + [spell],
                ))
            if 'Shield' not in effect_names:
                spell = 'Shield'
                q.put((turn + 1, hp, mana - 113, boss_hp, spent + 113,
                    effects + [(spell, 6)],
                    story + [spell],
                ))
            if 'Poison' not in effect_names:
                spell = 'Poison'
                q.put((turn + 1, hp, mana - 173, boss_hp, spent + 173,
                    effects + [(spell, 6)],
                    story + [spell],
                ))
            if 'Recharge' not in effect_names:
                spell = 'Recharge'
                q.put((turn + 1, hp, mana - 279, boss_hp, spent + 229,
                    effects + [(spell, 5)],
                    story + [spell],
                ))
        else:
            # boss turn
            hp -= max(1, boss_damage - armor)
            if hp <= 0:
                continue
            if mana <= 0:
                continue
            q.put((turn + 1, hp, mana, boss_hp, spent, effects, story))

        if hp <= 0:
            continue

    return best


def easy(hp, mana, boss_hp, boss_damage):
    return solve(hp, mana, boss_hp, boss_damage, is_hard=False)


def hard(hp, mana, boss_hp, boss_damage):
    return solve(hp, mana, boss_hp, boss_damage, is_hard=True)


# hp, attack, defense
print easy(50, 500, 55, 8)
print hard(50, 500, 55, 8)
# print hard(stats)
