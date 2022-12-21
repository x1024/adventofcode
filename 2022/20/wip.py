class Node:
  def __init__(self, value):
    self.value = value
    self.next = self.prev = None


def shift(node, shifts):
  prev, next = node.prev, node.next
  node.prev = node.next = None
  while shifts > 0: # This is guaranteed to be positive
    prev.next, next.prev = next, prev
    prev, next = next, next.next
    shifts -= 1
  prev.next = next.prev = node
  node.next, node.prev = next, prev
  return node


def solve(data, rounds=1, key=1):
  data = [Node(value * key) for value in data]
  l = len(data)
  for i in range(l):
    data[i].next = data[(i+1) % l]
    data[i].prev = data[(i-1) % l]

  # The modulo makes the shift always a positive value
  for _ in range(rounds):
    for cell in data: shift(cell, (cell.value % (l - 1)))

  start = next(cell for cell in data if cell.value == 0)
  for _ in range(1000): start = start.next
  res = start.value
  for _ in range(1000): start = start.next
  res += start.value
  for _ in range(1000): start = start.next
  res += start.value
  return res


data = [int(row.strip()) for row in open('input.txt', 'r').read().strip().split('\n')]
print(solve(data))
print(solve(data, 10, 811589153))