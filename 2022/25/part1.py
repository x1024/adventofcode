import IPython
import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()
data_test = '''
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''

digits = "210-="
numbers = '''
1=-0-2     1747
12111      906
2=0= 198
21       11
2=01      201
111       31
20012     1257
112       32
1=-1= 353
1-12      107
12        7
1= 3
122       37'''
numbers = [row.split() for row in numbers.strip("\n").split("\n")]
value = {
  '1': 1,
  '2': 2,
  '0': 0,
  '-': -1,
  '=': -2,
}

def convert(number):
  power = 1
  res = 0
  for i in number[::-1]:
    res += value[i] * power
    power *= 5
  return res

def deconvert(number):
  power = 1
  res = []
  while number > power * 2:
    number += power * 2
    power *= 5
  # print(power, number)
  # print("------")
  while power > 0:
    old_num = number
    # number += (power // 5) * 2
    # print(power, number)
    if number >= power * 2:
      number -= power * 2
      step = "2"
    elif number >= power:
      number -= power
      step = "1"
    elif number >= 0:
      step = "0"
    elif -power <= number < 0:
      number += power
      step = "-"
    else:
      number += power * 2
      step = "="
    res.append(step)
    power //= 5
    number -= power * 2

  res = ''.join(res)
  while res.startswith("0"): res = res[1:]
  return res

# data = data_test
data = data.strip("\n").split('\n')
data = [row.strip() for row in data]
result = sum(convert(row) for row in data)
print(result)
print(deconvert(result))

print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
