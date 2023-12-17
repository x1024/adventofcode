import functools


@functools.lru_cache(maxsize=None)
def solve(s, p):
    if not s: return not p
    if s[0] == '?': return solve(s[1:], p) + solve('#' + s[1:], p)
    elif s[0] == '.': return solve(s[1:], p)
    else: # if s[0] == '#':
        if not p: return 0
        block = p[0]
        if len(s) < block or any(s[i] == '.' for i in range(block)): return 0
        if len(s) > block and s[block] == '#': return 0
        return solve(s[block + 1:], p[1:])


def main(data, scale=1):
    return sum(solve(((spring + '?') * scale)[:-1], tuple(map(int, pattern.split(','))) * scale)
        for spring, pattern in (row.split() for row in data.split('\n')))


data = open('input.txt', 'r').read().strip()
print(main(data))
print(main(data, 5))
