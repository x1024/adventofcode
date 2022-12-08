import pprint
import collections
import numpy


def solve(input):
  stacks, commands = input
  for (num, _from, _to) in commands:
    stacks[_to] = stacks[_from][:num] + stacks[_to]
    stacks[_from] = stacks[_from][num:]
  return ''.join(stack[0] for stack in stacks)


def parse_line(input):
  return input.split()


def parse_command(row):
  cells = row.split(" ")
  return int(cells[1]), int(cells[3]) - 1, int(cells[5]) - 1

def parse_input(input):
  crates, commands = input.split('\n\n')
  commands = list(map(parse_command, commands.split("\n")))
  crates = crates.split("\n")[:-1]
  num = int((len(crates[0]) + 1) / 4)
  stacks = []
  for i in range(num): stacks.append([])
  for row in crates:
    for i in range(num):
      cell = (row[i*4+1])
      if cell != ' ':
        stacks[i].append(cell)

  return stacks, commands


def test():
  input = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2'''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

