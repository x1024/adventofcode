import IPython
import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()

data = data.split('\n')
data = [row.strip() for row in data]
data = [row for row in data if row]
# data = list(map(int, data))
# data = [row.split() for row in data]
asd = {}

while not 'root' in asd:
  for row in data:
    key, value = row.split(": ")
    try:
      value = int(value)
      asd[key] = value
    except:
      # print(value.split(" "))
      a, oper, b = value.split(" ")
      if a in asd and b in asd:
        asd[key] = eval("%s %s %s" % (asd[a], oper, asd[b]))
        # print("ASDASD")
      # print(a, oper, b)
print(len(asd))
print(asd['root'])
# print(asd)

result = 0



print(result)



print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
