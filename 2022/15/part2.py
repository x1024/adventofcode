import pprint
import collections
import numpy
import IPython


def solve(input, min_coord=0, max_coord=20):
  print_data(input)
  for y in range(0, max_coord + 1):
    ranges = []
    for sensor, beacon in input:
      distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
      dy = abs(sensor[1] - y)
      dx = distance - dy
      # print(y, sensor, beacon, distance, dy, dx, input_row, (sensor[0] - dx, sensor[0] + dx))
      ranges.append((sensor[0] - dx, sensor[0] + dx))

    ranges = list(sorted(ranges))
    r = ranges[0]
    i = 1
    l = len(ranges)
    if y % 1000 == 0:
      print(y)
    while i < l:
      r1 = ranges[i]
      if r1[0] - 1 > r[1]:
        # print(r, r1)
        if r[0] <= min_coord and r[1] >= max_coord:
          pass
          # print("END BAD", y, r, r1)
        else:
          # print("END", y, r, r1)
          x = r[1] + 1
          print(x, y)
          return x * 4000000 + y
          exit()
        break
      else:
        r = (min(r[0], r1[0]), max(r[1], r1[1]))
      i += 1

  res = (r[1] - r[0] + 1)
  return res


def print_data(input):
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
   print()



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
result = solve(input, 0, 4000000)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

IPython.embed()
