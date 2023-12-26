import math
import re

MAPPING = {'x': 0, 'm': 1, 'a': 2, 's': 3}

workflow_defs, initial_states = open('input.txt', 'r').read().strip().split("\n\n")

workflows = {}
for row in workflow_defs.split('\n'):
    if not row: continue
    name, workflow = row.replace("}", "").split("{")
    workflow = workflow.split(",")
    workflows[name] = [
        (MAPPING[var], sign, int(value), target) for var, sign, value, target in
        (re.findall("(.)(.)(\d+):(.+)", rule)[0] for rule in workflow[:-1])
    ] + [('!', '!', '!', workflow[-1])]

def solve(mins, maxs, workflow):
    if workflow == 'R': return 0
    if workflow == 'A': return math.prod(max(0, maxs[key] - mins[key] + 1) for key in range(len(MAPPING)))
    maxs = list(maxs)
    mins = list(mins)
    res = 0
    for var, sign, value, target in workflows[workflow]:
        if sign == '!':
            res += solve((mins), (maxs), target)
        elif sign == '<':
            old = maxs[var]
            maxs[var] = min(maxs[var], value - 1)
            res += solve((mins), (maxs), target)
            maxs[var] = old
            mins[var] = max(mins[var], value)
        else:
            old = mins[var]
            mins[var] = max(mins[var], value + 1)
            res += solve((mins), (maxs), target)
            mins[var] = old
            maxs[var] = min(maxs[var], value)
    return res

print(sum(sum(nums) * solve(nums, nums, 'in') for nums in (list(map(int, re.findall("\d+", row))) for row in initial_states.split('\n'))))
print(solve(list(1 for _ in range(len(MAPPING))), list(4000 for _ in range(len(MAPPING))), 'in'))
