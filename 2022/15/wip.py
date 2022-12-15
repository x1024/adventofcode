import pprint
import collections
import numpy
import IPython
import re

import PIL
from PIL import Image, ImageDraw


MOD = 4000000
def draw_input(input, target, limit, seen):
  size = 2000
  def point(x, y):
    lx = (x - minx) / dx
    ly = (y - miny) / dy
    # print(lx, ly)
    return round(size * lx), round(size * ly)
  
  def draw_ellipse(pos, color="red", radius=10):
    p = point(*pos)
    # print(p)
    draw.ellipse(((p[0] - radius, p[1] - radius), (p[0] + radius, p[1] + radius)), fill=color)

  img = Image.new("RGB", (size, size))
  minx, miny, maxx, maxy = input[0]
  for s0, s1, b0, b1 in input:
    dist = abs(s0 - b0) + abs(s1 - b1)
    x0, x1, = s0 - dist, s0 + dist
    y0, y1 = s1 - dist, s1 + dist
    minx = min(minx, x0, x1)
    maxx = max(maxx, x0, x1)
    miny = min(miny, y0, y1)
    maxy = max(maxy, y0, y1)
  # print(minx, maxx, miny, maxy)
  dx = maxx - minx
  dy = maxy - miny
  # print(dx, dy)

  draw = ImageDraw.Draw(img)
  for s0, s1, b0, b1 in input:
    dist = abs(s0 - b0) + abs(s1 - b1)
    x0, x1, = s0 - dist, s0 + dist
    y0, y1 = s1 - dist, s1 + dist
    draw.polygon((
      point(x0, s1),
      point(s0, y1),
      point(x1, s1),
      point(s0, y0),
    ), width=2)

  draw.polygon(( 
    point(0, limit),
    point(limit, limit),
    point(limit, 0),
    point(0, 0),
  ), width=2)
  # for x in range(-10, 20): for y in range(-10, 20): draw_ellipse((x, y), "white", 1)
  for s0, s1, b0, b1 in input:
    draw_ellipse((s0, s1), "blue", 10)
    draw_ellipse((b0, b1), "green", 10)
  draw_ellipse(target, "red", 20)
  for y in seen:
    draw_ellipse((0, y), "yellow", 5)
  img.show()
  # print_data(input)
  img.save("viz.png")



def solve(_input, min_coord=0, max_coord=20):
  input = [(s0, s1, abs(s0 - b0) + abs(s1 - b1)) for s0, s1, b0, b1 in _input]
  seen = []

  y = min_coord
  while y <= max_coord:
    seen.append(y)
    min_overlap = 99999999
    ranges = []
    for s0, s1, dist in input:
      dx = dist - abs(s1 - y)
      r = (s0 - dx, s0 + dx, s1)
      if r[0] > r[1]:
        # The rectangle will start in "this long"
        min_overlap = min(min_overlap, r[0] - r[1])
        continue
      ranges.append(r)

    # assume the range starts inside the valid coordinates
    range_end = ranges[0][1]
    max_s1 = ranges[0][2]
    for start, end, s1 in sorted(ranges):
      # The overlap will end in this long
      if not(max_s1 < y and s1 > y or max_s1 > y and s1 < y):
        # Only count rectangles that "are going in different directions"
        # That is, one is growing and the other one is shrinking.
        min_overlap = min(min_overlap, int(abs(start - range_end) / 2))
      if start > end: continue
      r1 = (start, end)
      if start - 1 > range_end:
        # The ranges no longer overlap
        if range_end < max_coord:
          # The range is inside the bounding box
          x = range_end + 1
          print(x, y, r, r1)
          draw_input(_input, (x, y), max_coord, seen)
          return x * MOD + y
        break
      else:
        if end > range_end:
          range_end = end
          max_s1 = s1
    if min_overlap > 0:
      print("%5.2f%% %d" % (100 * y/max_coord, y))
    y += min_overlap + 1


def parse_line(input):
  return tuple(map(int, re.findall("[-\d]+", input)))


def parse_input(input):
  return list(map(parse_line, input.split('\n')))

def print_data(input):
 for y in range(-10, 30):
   print("%02d " % y, end="")
   for x in range(-10, 30):
     pos = (x, y)
     cell = '.'
     for row in input:
       sensor, beacon = row[:2], row[2:]
       distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
       dpos = abs(sensor[0] - pos[0]) + abs(sensor[1] - pos[1])
       if sensor == pos:
         cell = "S"
       elif beacon == pos:
         cell = "B"
       elif dpos <= distance and cell == '.':
         cell = "#"
     print(cell, end="")
   print()


def test():
  input = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
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
Sensor at x=17, y=20: closest beacon is at x=21, y=22'''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


do_test = True
do_test = False
if do_test:
  test()
else:
  input = open('input.txt', 'r').read().strip()
  input = parse_input(input)
  result = solve(input, 0, 4_000_000)
  print("Result: {}".format(result))

  import pyperclip
  pyperclip.copy(str(result))

  # IPython.embed()