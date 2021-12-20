#!/usr/bin/env python
#-*- coding: UTF-8 -*-

def parse_line(line):
    line = line.split(' ')
    if line[0] == 'swap':
        if line[1] == 'position':
            return swap_pos, int(line[2]), int(line[5])
        if line[1] == 'letter':
            return swap_letter, line[2], line[5]
    if line[0] == 'rotate':
        if line[1] == 'based':
            return rotate_letter, line[6]
        elif line[1] == 'left':
            return rotate_left, int(line[2])
        else:
            return rotate_right, int(line[2])
    if line[0] == 'reverse':
        return reverse, int(line[2]), int(line[4])
    if line[0] == 'move':
        return move, int(line[2]), int(line[5])
    raise NotImplementedError()


def parse_line_reverse(line):
    line = line.split(' ')
    if line[0] == 'swap':
        if line[1] == 'position':
            return swap_pos, int(line[2]), int(line[5])
        if line[1] == 'letter':
            return swap_letter, line[2], line[5]

    if line[0] == 'rotate':
        if line[1] == 'based':
            return rotate_letter_reverse, line[6]
        elif line[1] == 'left':
            return rotate_right, int(line[2])
        else:
            return rotate_left, int(line[2])
    if line[0] == 'reverse':
        return reverse, int(line[2]), int(line[4])
    if line[0] == 'move':
        return move, int(line[5]), int(line[2])
    raise NotImplementedError()


def parse_input(data, reverse=False):
    callback = parse_line_reverse if reverse else parse_line
    return [callback(row) for row in data.split("\n")[::(-1 if reverse else 1)]]


def swap_pos(word, i, j):
    tmp = word[i]
    word[i] = word[j]
    word[j] = tmp
    return word


def swap_letter(word, i, j):
    return list(''.join(word).replace(i, '-').replace(j, i).replace('-', j))


def rotate_left(word, i):
    return word[i % len(word):] + word[:i % len(word)]


def rotate_right(word, i):
    return rotate_left(word, len(word) - i)


def rotate_letter_reverse(word, letter):
    for i in range(len(word)):
        word_rotated = rotate_left(word, i)
        if rotate_letter(word_rotated, letter) == word:
            return word_rotated


def rotate_letter(word, letter):
    index = word.index(letter)
    return rotate_right(word, 1 + index + (index >= 4))


def reverse(word, i, j):
    return word[:i] + word[i:j+1][::-1] + word[j+1:]


def move(word, i, j):
    tmp = word.pop(i)
    word.insert(j, tmp)
    return word


def apply_command(string, row):
    return row[0](string, *row[1:])

def solve(string, data, reverse=False):
    return ''.join(reduce(apply_command, parse_input(data, reverse=reverse), list(string)))


def easy(string, data):
    return solve(string, data)


def hard(string, data):
    return solve(string, data, reverse=True)


def test():
    data = '''swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d'''
    assert easy('abcde', data) == 'decab'
    # assert hard(data, 10) == 2


def main():
    import sys
    test()
    data = sys.stdin.read()
    key = 'abcdefgh'
    print easy(key, data)

    key2 = 'fbgdceah'
    print hard(key2, data)
    assert easy(hard(key2, data), data) == key2


if __name__ == '__main__':
    main()