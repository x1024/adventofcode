import IPython
import collections
import numpy
import pprint
import re

data = open('input.txt', 'r').read().strip()
data_test = '''
1
2
-3
3
-2
0
4
'''
# data = data_test

data = data.split('\n')
data = [row.strip() for row in data]
data = [row for row in data if row]
# data = list(map(lambda row: list(map(int, re.findall("\d+", row))), data))
data = list(map(int, data))
# data = [row.split() for row in data]
# data = list(enumerate(data))

class Node:
  def __init__(self, value):
    self.value = value
    self.index = 0
    self.next = None
    self.prev = None

list = None
l = [Node(cell) for cell in data]
for i in range(len(l)):
  l[i].index = i
  l[i].next = l[(i+1) % len(l)]
  l[i].prev = l[(i-1 + len(l)) % len(l)]

expected = [1, 2, -3, 4, 0, 3, -2]
pprint.pprint(data)
result = 0

def shift(node):
  size = node.value
  old_prev = node.prev
  old_next = node.next
  node.prev = None
  node.next = None

  if size > 0:
    for x in range(size):
      old_prev.next = old_next
      old_next.prev = old_prev
      old_prev = old_next
      old_next = old_next.next
  elif size < 0:
    for x in range(-size):
      old_prev.next = old_next
      old_next.prev = old_prev
      old_next = old_prev
      old_prev = old_next.prev
  old_prev.next = node
  old_next.prev = node
  node.next = old_next
  node.prev = old_prev

  # print(size, node.index)
  return node

def print_arr(arr):
  start_index = arr.index
  while True:
    print(arr.value, end=" ")
    arr = arr.next
    if arr.index == start_index: break
  print()

p = l[0]
start = l[0]
print_arr(start)
for x in range(len(data)):
  index = 0
  while True:
    if start.index == x:
      # print(start.value)
      start = shift(start)
      # print_arr(p)
      break
    else:
      start = start.next

while start.value != 0: start = start.next
res = []
for i in range(1000):
  start = start.next
res.append(start.value)
for i in range(1000):
  start = start.next
res.append(start.value)
for i in range(1000):
  start = start.next
res.append(start.value)
print(res)
result = (sum(res))

print("Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

IPython.embed()
