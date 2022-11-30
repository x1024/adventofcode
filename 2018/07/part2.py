import pprint
import collections
import numpy


def solve(input, workers=5, step_duration=60):
  data = collections.defaultdict(lambda: set())
  for key, val in input:
    data[val].add(key)
  # pprint.pprint(data)
  parts = list(sorted(set([i[0] for i in input] + [i[1] for i in input])))
  # print(parts)
  done = []
  started = set()
  time = -1
  todo = []

  while True:
    time += 1
    # print(time, len(done), done, todo)

    for (t, part) in todo:
      # print(t, time, part)
      if time >= t:
        done.append(part)
        for p in data.values():
          if part in p:
            p.remove(part)
        break
    todo = [t for t in todo if time < t[0]]

    if len(done) >= len(parts): break

    for part in parts:
      if part in started: continue
      if len(data[part]) == 0 and len(todo) < workers:
        duration = step_duration + ord(part) - ord('A') + 1
        started.add(part)
        todo.append((time + duration, part))

  return time
  # return ''.join(done)


def parse_line(input):
  parts = input.split()
  return parts[1], parts[7]


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input

def test():
  input = '''
Step C must be finished before step A can begin.  
Step C must be finished before step F can begin.  
Step A must be finished before step B can begin.  
Step A must be finished before step D can begin.  
Step B must be finished before step E can begin.  
Step D must be finished before step E can begin.  
Step F must be finished before step E can begin.
  '''
  input = parse_input(input)
  result = solve(input, 2, 0)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
