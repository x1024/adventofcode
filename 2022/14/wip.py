import pprint
import collections
import numpy
import IPython
import glob
from PIL import Image, ImageDraw

'''
ffmpeg -framerate 120 -pattern_type glob -i 'images/*.png' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -pix_fmt yuv420p out_120.mp4
ffmpeg -i out_120.mp4 -filter:v scale=-1:720 -c:a copy out_120_scaled.mp4                          10:45
'''

EMPTY = 0
WALL = 1
SAND = 2

# EMPTY = ' '
# WALL = '█'
# SAND = 'o'

make_video = False
make_video = True
frame = 0
image = None

def init_image(data, max_y):
  global image
  max_y += 10
  size = (max_y * 2, max_y)
  image = Image.new("RGB", size, "black")
  color = (255, 255, 255)
  min_x = 500 - max_y
  max_x = 500 + max_y
  for (x, y) in data:
    cell = data[x, y]
    if x < min_x or x >= max_x: continue
    # if y == max_y + 2: cell = WALL
    if cell == WALL:
      image.putpixel((x - min_x, y), color)
  return image


def update_image(sand, max_y):
  global frame
  global image
  image.putpixel(sand, (255, 0, 0))
  image.save("images/%05d.png" % frame)
  frame += 1


def solve(data):
  sand = 0
  start = (500, 0)

  first_dropped_sand = 0
  max_y = max(y for (_, y) in data.keys())

  # Only needed for drawing the image
  min_x = start[0] - (max_y + 10)
  max_x = start[0] + (max_y + 10)
  # for x in range(min_x, max_x + 1): data[x, max_y + 2] = WALL
  if make_video: init_image(data, max_y)

  while True:
    x, y = start
    if make_video:
      print(frame)
    while True:
      if y == max_y + 1:
        if not first_dropped_sand: first_dropped_sand = sand
        data[(x, y)] = SAND
        sand += 1
        break
      elif data[(x, y+1)] == EMPTY:
        y = y + 1
      elif data[(x-1, y+1)] == EMPTY:
        x = x - 1
        y = y + 1
      elif data[(x+1, y+1)] == EMPTY:
        x = x + 1
        y = y + 1
      else:
        data[(x, y)] = SAND
        sand += 1
        if make_video:
          update_image((x - min_x, y), max_y)
        if (x, y) == start:
          if make_video:
            # Add a few empty frames at the end
            for _ in range(100):
              update_image((x - min_x, y), max_y)
          return first_dropped_sand, sand
        break


def parse_line(input):
  input = input.split(" -> ")
  input = [tuple(map(int, row.split(","))) for row in input]
  return input


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  data = collections.defaultdict(lambda: EMPTY)
  for row in input:
    x, y = row[0]
    for nx, ny in row[1:]:
      for _x in range(min(x, nx), max(x, nx) + 1):
        for _y in range(min(y, ny), max(y, ny) + 1):
          data[(_x, _y)] = WALL
      x, y = nx, ny
  return data



def test():
  input = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

# IPython.embed()