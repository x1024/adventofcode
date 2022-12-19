import IPython
import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()
data_test = '''
'''
# data = data_test
data = data.split('\n')
data = [row.strip() for row in data]
data = [row for row in data if row]
# data = list(map(int, data))
data = [row.split() for row in data]

pprint.pprint(data)
result = 0
print(result)



print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
