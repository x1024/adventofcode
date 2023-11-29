import pprint
import collections
import numpy


opcodes = {
  'addr': (lambda a, b, r: r[a] + r[b]),
  'addi': (lambda a, b, r: r[a] + b),
  'mulr': (lambda a, b, r: r[a] * r[b]),
  'muli': (lambda a, b, r: r[a] * b),
  'divr': (lambda a, b, r: r[a] // r[b]),
  'divi': (lambda a, b, r: r[a] // b),
  'banr': (lambda a, b, r: r[a] & r[b]),
  'bani': (lambda a, b, r: r[a] & b),
  'borr': (lambda a, b, r: r[a] | r[b]),
  'bori': (lambda a, b, r: r[a] | b),
  'setr': (lambda a, b, r: r[a]),
  'seti': (lambda a, b, r: a),
  'gtir': (lambda a, b, r: int(a > r[b])),
  'gtri': (lambda a, b, r: int(r[a] > b)),
  'gtrr': (lambda a, b, r: int(r[a] > r[b])),
  'eqir': (lambda a, b, r: int(a == r[b])),
  'eqri': (lambda a, b, r: int(r[a] == b)),
  'eqrr': (lambda a, b, r: int(r[a] == r[b])),
}


def solve(data, registers = (0, 0, 0, 0, 0, 0)):
  registers = list(registers)
  _ip_reg = [row for row in data if row[0] =='#ip']
  data = [(row[0], int(row[1]), int(row[2]), int(row[3])) for row in data if row not in _ip_reg]
  ip_register = int(_ip_reg[0][1])
  ip = registers[ip_register]
  done = False
  seen = set()
  last = 0

  while True:
    if not (0 <= ip < len(data)): break
    registers[ip_register] = ip
    opcode, a, b, c = command = data[ip]
    if opcode != 'noop':
      registers[c] = opcodes[opcode](a, b, registers)
    if ip == 28:
      value = registers[1]
      if value in seen:
        print(seen)
        print(last)
        exit()
      seen.add(value)
      last = value
      print("%05d %s" % (len(seen), registers))
    ip = registers[ip_register]
    ip += 1
  # for row in data:
  print(registers)
  # pprint.pprint(data)
  return 0


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


data = open('input3.txt', 'r').read().strip()
data = parse_input(data)
# result = solve(data, registers=(7723681, 0, 0, 0, 0, 0))
result = solve(data, registers=(0, 0, 0, 0, 0, 0))

print("Result: {}".format(result))
