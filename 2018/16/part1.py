import pprint
import collections
import numpy


def solve(input):
  # pprint.pprint(input)
  result = 0
  for row in input:
    before, code, after = row
    possible = 0
    for opcode in opcodes:
      registers = before.copy()
      op, a, b, c = code
      registers[c] = opcodes[opcode](a, b, registers)
      # print(opcode, registers, after, registers == after)
      if registers == after:
        possible += 1
    print(possible, row)
    if possible >= 3:
      result += 1
  return result

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
  'gtri': (lambda a, b, r: int(r[a] > r[b])),
  'gtrr': (lambda a, b, r: int(r[a] > b)),
  'eqir': (lambda a, b, r: int(a == r[b])),
  'eqri': (lambda a, b, r: int(r[a] == b)),
  'eqrr': (lambda a, b, r: int(r[a] == r[b])),
}

def command(registers, opcode, a, b, c):
  registers[c] = opcodes[opcode](a, b, registers)


def parse_line(input):
  before = list(map(int, input[0].replace('Before: [', '').replace(']', '').split(', ')))
  code = list(map(int, input[1].split()))
  after = list(map(int, input[2].replace('After:  [', '').replace(']', '').split(', ')))
  return before, code, after


def parse_input(input):
  samples, code = input.split('\n\n\n')
  samples = samples.split('\n\n')
  samples = [sample.split('\n') for sample in samples]
  samples = list(map(parse_line, samples))
  return samples


def test():
  input = '''
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
