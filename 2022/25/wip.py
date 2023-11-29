digits = "=-012"
def convert(number): return sum((digits.index(c) - 2) * (5**i) for i, c in enumerate(number[::-1]))
def deconvert(number): return '' if not number else digits[(number + 2) % 5] + deconvert(number // 5)
print(deconvert(sum(convert(row) for row in open('input.txt', 'r').read().splitlines())))