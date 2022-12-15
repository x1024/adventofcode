import functools
from math import prod

def cmp(a, b):
  if type(a) == int and type(b) == int: return b - a
  if type(a) == int: a = [a]
  if type(b) == int: b = [b]
  return next(
    filter((lambda x: x), (cmp(_a, _b) for _a, _b in zip(a, b))), # get first non-zero result
    len(b) - len(a)) # or just compare lengths instead


def easy(input):
  return sum((i + 1) * (cmp(a, b) > 0) for i, (a, b) in enumerate(input))


def hard(input):
  dividers = [[[2]], [[6]]]
  data = list(reversed(sorted(sum(input, dividers), key=functools.cmp_to_key(cmp))))
  return prod([data.index(divider) + 1 for divider in dividers])


input = open('input.txt', 'r').read().strip()
input = [[eval(row) for row in group.split('\n')] for group in input.split('\n\n')]
print(easy(input))
print(hard(input))