import re

values = [
    '1', 'one',
    '2', 'two',
    '3', 'three',
    '4', 'four',
    '5', 'five',
    '6', 'six',
    '7', 'seven',
    '8', 'eight',
    '9', 'nine',
]
re_left = "(%s)" % "|".join(values)
re_right = ".*(%s).*?" % "|".join(values)

def val(row, regex, index):
    value = values.index([r.groups() for r in re.finditer(regex, row)][index][0])
    return values[value // 2 * 2]

print(sum(int(val(row, re_left, 0) + val(row, re_right, -1))
    for row in open('input.txt', 'r').read().strip().split('\n')))