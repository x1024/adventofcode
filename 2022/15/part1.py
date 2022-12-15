import pprint
import collections
import numpy
import IPython


def solve(input, input_row=10):
  data = {}
  result = 0
  min_x = 0
  max_x = 0
  for sensor, beacon in input:
    data[sensor] = "S"
    data[beacon] = "B"
    distance = sensor[0] - beacon[0] + sensor[1] - beacon[1]
    min_x = min(min_x, sensor[0] - distance)
    max_x = max(max_x, sensor[0] - distance)
    # print(sensor, beacon, distance)
  y = input_row

  res = set()
  for sensor, beacon in input:
    distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    dy = abs(sensor[1] - y)
    dx = distance - dy
    print(y, sensor, beacon, distance, dy, dx, input_row, (sensor[0] - dx, sensor[0] + dx))
    for x in range(sensor[0] - dx, sensor[0] + dx + 1):
      res.add(x)

  for y in range(-5, 30):
    print("%02d " % y, end="")
    for x in range(-5, 30):
      pos = (x, y)
      cell = '.'
      for sensor, beacon in input:
        distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        dpos = abs(sensor[0] - pos[0]) + abs(sensor[1] - pos[1])
        if sensor == pos:
          cell = "S"
        elif beacon == pos:
          cell = "B"
        elif dpos <= distance:
          cell = "#"
      print(cell, end="")
      if cell == "#": result += 1
    print()

  print(sorted(res))
  for sensor, beacon in input:
    if sensor[1] == input_row and sensor[0] in res:
      res.remove(sensor[0])
    if beacon[1] == input_row and beacon[0] in res:
      res.remove(beacon[0])
  print(len(res))
  return len(res)
    

  return result


def parse_line(input):
  sensor, beacon = input.split(":")
  sensor = sensor.replace(",","").split()[-2:]
  sensor = int(sensor[0].split("=")[-1]), int(sensor[1].split("=")[-1])
  beacon = beacon.replace(",","").split()[-2:]
  beacon = int(beacon[0].split("=")[-1]), int(beacon[1].split("=")[-1])
  return (sensor, beacon)


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
Sensor at x=17, y=20: closest beacon is at x=21, y=22
  '''
  # input = ''' Sensor at x=8, y=7: closest beacon is at x=2, y=10 '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input, 2000000)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

IPython.embed()
