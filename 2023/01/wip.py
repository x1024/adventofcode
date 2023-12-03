import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()
# data_test = open('input-sample.txt', 'r').read().strip()

# data = data_test
_data = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''

data = data.split('\n')
data = [row.strip() for row in data]
data = [row for row in data if row]
# data = list(map(int, data))

r = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

values = [
    'one', '1',
    'two', '2',
    'three', '3',
    'four', '4',
    'five', '5',
    'six', '6',
    'seven', '7',
    'eight', '8',
    'nine', '9',
]

r = { 'one': '1',
     'two': '2',
     'three': '3',
     'four': '4',
     'five': '5',
     'six': '6',
     'seven': '7',
     'eight': '8',
     'nine': '9',
     '1': '1',
     '2': '2',
     '3': '3',
     '4': '4',
     '5': '5',
     '6': '6',
     '7': '7',
     '8': '8',
     '9': '9',
     }


sum =0 
for row in data:
    left = [(row.find(v), v) for v in values]
    left = min([l for l in left if l[0] != -1])
    right = [(row.rfind(v), v) for v in values]
    right = max([l for l in right if l[0] != -1])
    print(left, right)
    sum += int(r[left[1]] + r[right[1]])
    # print(r1)
    # print(row)
    # print(res)
    # print()
    # input()
# pprint.pprint(data)
result = sum
print(result)



print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

import IPython
IPython.embed()
