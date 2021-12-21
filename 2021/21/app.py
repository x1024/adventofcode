#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import collections


def get_moves():
    return list(collections.Counter(sum((x+1, y+1, z+1))
        for x in range(3)
        for y in range(3)
        for z in range(3)
    ).items())


def hard(players, LIMIT = 21, SIZE = 10):
    def make_move(state, move):
        position, score = state
        position = (position + move) % SIZE
        score = score + position + 1
        return (position, score)
    
    def is_winning(state, player):
        return state[player][1] >= LIMIT

    def simulate_all_moves(states, player):
        wins = 0
        new_states = collections.defaultdict(lambda: 0)
        for move, move_count in moves:
            for state, universes in states.items():
                state = list(state)
                state[player] = make_move(state[player], move) 
                state = tuple(state)
                if is_winning(state, player):
                    wins += universes * move_count
                else:
                    new_states[state] += universes * move_count
        return wins, new_states

    moves = get_moves()
    states = collections.defaultdict(lambda: 0)
    pos1, pos2 = players
    initial_state = ((pos1-1, 0), (pos2-1, 0))
    states[initial_state] = 1
    wins1 = 0
    wins2 = 0

    while len(states):
        wins, states = simulate_all_moves(states, 0)
        wins1 += wins
        wins, states = simulate_all_moves(states, 1)
        wins2 += wins
    return wins1


def easy(players, LIMIT = 1000, SIZE = 10):
    pos1, pos2 = players
    state = [(pos1 - 1, 0), (pos2 - 1, 0)]
    rolls = 0

    def do_move(state, move):
        pos, score = state
        pos = (pos + move) % SIZE
        score = score + pos + 1
        return (pos, score)

    def is_winning(state):
        return any(score >= LIMIT for (_, score) in state)

    while True:
        state[0] = do_move(state[0], 3 * rolls + 6)
        rolls += 3
        if is_winning(state): break

        state[1] = do_move(state[1], 3 * rolls + 6)
        rolls += 3
        if is_winning(state): break

    return min(score for (_, score) in state) * rolls



def test():
    data = (4, 8)
    assert easy(data) == 739785
    assert hard(data) == 444356092776315


def main():
    test()
    data = map(int, (row.split()[-1] for row in open('in.txt').read().split('\n')))
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()