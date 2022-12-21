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

d = []
for row in data:
  key, value = row.split(": ")
  try:
    value = int(value)
    asd[key] = value
  except:
    a, oper, b = value.split(" ")
    d.append((key, a, oper, b))
    pass

START = 6873767042180
START = 3740214169900
q = asd
for i in range(START, START * 10):
  asd = dict(q)
  # print(asd)
  asd['humn'] = i
  done = False
  # while 'root' not in asd:
  print(i)
  while not done:
    for key, a, oper, b in d:
      if a in asd and b in asd:
        if key == 'root':
          print('ROOT', asd[b] - asd[a], asd[a], asd[b])
          done = True
          if asd[a] == asd[b]:
            print(i)
            exit()
          else:
            break
        asd[key] = int(eval("%s %s %s" % (asd[a], oper, asd[b])))
        # print(a, oper, b)
# print(len(asd))
# print(asd['root'])
# print(asd)

result = 0



print(result)



print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
