import re
import functools

def hash(string): return functools.reduce(lambda cur, s: ((cur + ord(s)) * 17) % 256, string, 0)


data = open('input.txt', 'r').read().strip()
boxes = [[] for _ in range(256)]
for k, v in [re.findall(r'^(\w+)[=-](\d*)$', p)[0] for p in data.split(',')]:
    box = boxes[hash(k)]
    if not list(map(box.pop if not v else lambda i: box.__setitem__(i, (k,int(v))), ( i for i, b in enumerate(box) if b[0] == k ))) and v:
        box.append([k, int(v)])

print(sum([hash(p) for p in data.split(',')]))
print(sum(sum((b+1) * (i+1) * int(v) for i, (k, v) in enumerate(boxes[b])) for b in range(len(boxes))))
