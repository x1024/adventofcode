def parse_line(line):
  # Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
  words = line.strip(".").split()
  name = words[0]
  km = int(words[3])
  s1 = int(words[6])
  s2 = int(words[-2])
  return (name, km, s1, s2)

def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = map(parse_line, input)
  print input
  # input = [row for row in input if row]
  # input = map(int, input)
  return input

def simulate(config, seconds):
  name, km, s1, s2 = config
  is_resting = False
  temp = s1
  distance = 0
  while seconds > 0:
    seconds -= 1
    temp -= 1
    if not is_resting:
      distance += km
    if temp == 0:
      if is_resting:
        temp = s1
      else:
        temp = s2
      is_resting = not is_resting
  return distance


def solve(input, seconds):
  points = {}
  for second in range(1, seconds + 1):
    distances = {}
    for row in input:
      name = row[0]
      distances[name] = simulate(row, second)
    maxdist = max(distances.values())
    for name, val in distances.items():
      if val == maxdist:
        points[name] = points.get(name, 0) + 1
    # return maxdist
  print max(points.values())

input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input, 2503)
# result = solve(input, 1000)
# result = solve(input, 3)
print("Result: {}".format(result))
