import pprint
import collections

def solve(state, steps, data):
  tape = collections.defaultdict(lambda: 0)
  pos = 0
  while steps > 0:
    val = tape[pos]
    write, move, new_state = data[state][val]

    tape[pos] = write
    pos += -1 if move == 'left' else 1
    state = new_state

    steps -= 1
  print(state, pos, [tape[i] for i in range(-5, 5)])
  return sum(tape.values())


def parse_line(input):
  return input.split()


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  header = input[:2]
  start = header[0].split(" ")[-1].strip(".")
  steps = int(header[1].split(" ")[-2].strip("."))
  # print(start, steps)
  code = input[2:]
  data = {}
  for chunk in range(0, len(code), 9):
    segment = [row.split(" ") for row in code[chunk:chunk+9]]
    state = segment[0][-1].strip(":")
    write_1 = int(segment[2][-1].strip("."))
    move_1 = segment[3][-1].strip(".")
    continue_1 = segment[4][-1].strip(".")

    write_2 = int(segment[6][-1].strip("."))
    move_2 = segment[7][-1].strip(".")
    continue_2 = segment[8][-1].strip(".")
    # print(state, write_1, move_1, continue_1)
    # print(state, write_2, move_2, continue_2)
    data[state] = {
      0: [write_1, move_1, continue_1],
      1: [write_2, move_2, continue_2]
    }
  # input = list(map(int, input))
  # input = map(parse_line, input)
  return start, steps, data


def test():
  input = '''
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
  '''
  start, steps, data = parse_input(input)
  result = solve(start, steps, data)
  assert result == 3


test()
input = open('input.txt', 'r').read().strip()
start, steps, data = parse_input(input)
result = solve(start, steps, data)
print("Result: {}".format(result))
