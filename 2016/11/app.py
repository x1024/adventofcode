#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import collections
import itertools
import queue


TYPE_MICROCHIP = 1
TYPE_GENERATOR = 2
TYPE_PLAYER = 3


def parse_input(data):
    result = []
    names = {}
    for row in data.split('\n'):
        if 'nothing relevant' in row:
            result.append([])
            continue
        row = (row.strip('.')
            .replace(' an ', " a ")
            .replace(', a ', "|")
            .replace(', and a ', "|")
            .replace(' and a ', '|'))
        items = row.split('contains a ')[1].split('|')
        items_parsed = []
        for item in items:
            if 'microchip' in item:
                name = item.split('-compatible')[0]
                type = TYPE_MICROCHIP
            else:
                name = item.split()[0]
                type = TYPE_GENERATOR
            if name in names:
                code = names[name]
            else:
                code = names[name] = len(names)
            items_parsed.append((code, type))
        result.append(items_parsed)

    floors = tuple(map(make_floor, result))
    player_floor = 0
    return (player_floor, floors)


def make_floor(floor):
    return tuple(sorted(floor))


def is_valid_floor(floor):
    chips = [name for (name, type) in floor if type == TYPE_MICROCHIP]
    generators = [name for (name, type) in floor if type == TYPE_GENERATOR]
    return len(generators) == 0 or all((chip, TYPE_GENERATOR) in floor for chip in chips)


def is_valid_state(floors):
    return all(is_valid_floor(floor) for floor in floors)


def moves(state):
    player_floor, floors = state
    current_floor = floors[player_floor]

    combinations = (
        list(itertools.combinations(current_floor, 1)) +
        list(itertools.combinations(current_floor, 2))
    )

    for c in combinations:
        new_current_floor = make_floor(set(current_floor) - set(c))
        if player_floor > 0:
            new_floors = list(floors)
            new_floors[player_floor] = new_current_floor
            new_floors[player_floor - 1] = make_floor(floors[player_floor - 1] + c)
            if is_valid_state(new_floors):
                yield (player_floor - 1, tuple(new_floors))

        if player_floor < len(floors) - 1:
            new_floors = list(floors)
            new_floors[player_floor] = new_current_floor
            new_floors[player_floor + 1] = make_floor(floors[player_floor + 1] + c)
            if is_valid_state(new_floors):
                yield (player_floor + 1, tuple(new_floors))


def print_state(state):
    print "---------"
    player_floor, floors = state
    for i, floor in reversed(list(enumerate(floors))):
        row = []
        row.append('%s ' % i)
        if player_floor == i:
            row.append('P')
        else:
            row.append(' ')
        for (a, b) in floor:
            if b == TYPE_GENERATOR:
                t = 'G'
            else:
                t = 'M'
            row.append(' %s%s' % (a, t))
        print ''.join(row)
    print "---------"
            

def solve(data):
    initial_state = parse_input(data)
    _, floors = initial_state
    final_floors = list(tuple() for i in range(len(floors) - 1))
    final_floor = make_floor(sum(floors, tuple()))
    final_floors.append(final_floor)
    final_floors = tuple(final_floors)
    final_state = (len(floors) - 1, final_floors)

    print_state(initial_state)
    print_state(final_state)

    q = queue.Queue()
    q.put((0, initial_state))
    seen = {}
    seen[initial_state] = 0

    i = 0
    while not q.empty():
        steps, state = q.get()
        i += 1
        if i % 1000 == 0:
            print steps, len(seen), q.qsize()
        if state == final_state:
            print steps
            print_state(state)
            return steps
        for move in moves(state):
            if move in seen: continue
            seen[move] = steps
            q.put((steps + 1, move))


def easy():
    data = '''The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip.
The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
The third floor contains a thulium-compatible microchip.
The fourth floor contains nothing relevant.'''
    return solve(data)



def hard():
    data = '''The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, a plutonium-compatible microchip, an elerium generator, an elerium-compatible microchip, a dilithium generator, and a dilithium-compatible microchip
The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
The third floor contains a thulium-compatible microchip.
The fourth floor contains nothing relevant.'''
    return solve(data)


def test():
    data = '''The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.'''
    assert solve(data) == 11


if __name__ == '__main__':
    test()
    print easy()
    print hard()