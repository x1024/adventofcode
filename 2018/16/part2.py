import pprint
import collections
import numpy


def solve(samples, source_code):
  found_opcodes = {}
  found_opcodes_reverse = {}
  while len(found_opcodes) < len(opcodes):
    for row in samples:
      before, code, after = row
      op, a, b, c = code
      if op in found_opcodes: continue

      possible = []
      for opcode in opcodes:
        if opcode in found_opcodes_reverse: continue
        registers = before.copy()
        registers[c] = opcodes[opcode](a, b, registers)
        # print(opcode, registers, after, registers == after)
        if registers == after:
          possible.append(opcode)
      if len(possible) == 1:
        # print(op, possible, len(found_opcodes))
        found_opcodes[op] = possible[0]
        found_opcodes_reverse[possible[0]] = op

  # print(found_opcodes)
  registers = [0, 0, 0, 0]
  for row in source_code:
    op, a, b, c = row
    # print(row)
    opcode = found_opcodes[op]
    registers[c] = opcodes[opcode](a, b, registers)
  print(registers)
  return 0

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
  samples, code = input.split('\n\n\n\n')
  samples = samples.split('\n\n')
  samples = [sample.split('\n') for sample in samples]
  samples = list(map(parse_line, samples))

  code = [list(map(int, row.split())) for row in code.split("\n") if row]
  return samples, code


def test():
  input = '''
  '''
  samples, code = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
input = open('input.txt', 'r').read().strip()
samples, code = parse_input(input)
result = solve(samples, code)
print("Result: {}".format(result))
