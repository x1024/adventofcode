import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()
# data_test = open('input-sample.txt', 'r').read().strip()

# data = data_test

data = data.split('\n')
data = [row.strip() for row in data]
data = [row for row in data if row]
# data = list(map(int, data))

sum =0 
for row in data:
    res = ''
    for c in row:
        if c >='0' and c <='9':
            res += c
    res = res[0] + res[-1]
    sum += int(res)
    print(res)
pprint.pprint(data)
result = sum
print(result)



print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

import IPython
IPython.embed()
