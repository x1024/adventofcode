import numpy as np
def extrapolate(nums): return nums[-1] + extrapolate(np.diff(nums)) if nums.any() else 0
data = [list(map(int, row.split())) for row in open('input.txt', 'r').read().strip().split('\n')]
print(sum(map(extrapolate, np.array(data))))
print(sum(map(extrapolate, np.array([r[::-1] for r in data]))))
