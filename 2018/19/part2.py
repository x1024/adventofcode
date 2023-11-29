import pprint
import collections
import numpy

opcodes = {
  'addr': (lambda a, b, r: r[a] + r[b]),
  'addi': (lambda a, b, r: r[a] + b),
  'mulr': (lambda a, b, r: r[a] * r[b]),
  'muli': (lambda a, b, r: r[a] * b),
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

  while True:
    if not (0 <= ip < len(data)): break
    registers[ip_register] = ip
    # print(ip)
    if ip == 7:
      print("%02d" % ip, len(data), registers, end=" ")
    opcode, a, b, c = command = data[ip]
    if ip == 7:
      print(command, end=" ")
    registers[c] = opcodes[opcode](a, b, registers)
    if ip == 7:
      print(registers)
      input()
    ip = registers[ip_register]
    ip += 1
  # for row in data:
  print(registers)
  # pprint.pprint(data)
  return 0


def parse_line(input):
  return input.split()


def divisor_sum(n):
  return sum(i + n // i for i in range(1, int(n**0.5) + 1) if n % i == 0)


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  data = '''#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5'''
  data = parse_input(data)
  result = solve(data)
  print("Test Result: {}".format(result))
  exit()


# test()
data = open('input.txt', 'r').read().strip()
data = parse_input(data)
# result = solve(data)

print(divisor_sum(896))
print(divisor_sum(10551296))