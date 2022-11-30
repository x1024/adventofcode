import pprint
import collections
import numpy

def move(point, time):
  pos, vel = point
  p = (pos[0] + vel[0] * time, pos[1] + vel[1] * time)
  return (p, vel)


def solve(inp):
  i = 0
  x = [p[0][0] for p in inp]
  # y = [p[0][1] for p in inp]
  besti = 0
  mindx = max(x) - min(x)
  # mindy = max(y) - min(y)

  while True:
    # i += int(input())
    data = [move(point, i) for point in inp]
    x = [p[0][0] for p in data]
    y = [p[0][1] for p in data]
    dx = max(x) - min(x)
    # dy = max(y) - min(y)
    if dx <= mindx:
      mindx = dx
      besti = i
      print(i, dx)
    else:
      break
    i += 1
  data = [move(point, besti) for point in inp]
  x = [p[0][0] for p in data]
  y = [p[0][1] for p in data]
  dx = max(x) - min(x)
  dy = max(y) - min(y)
  print(dx, dy)

  print_board(data)

  return 0


def print_board(data):
  x = [p[0][0] for p in data]
  y = [p[0][1] for p in data]
  mx = min(x)
  my = min(y)
  dx = max(x) - min(x)
  dy = max(y) - min(y)
  board = []
  for _ in range(dy + 1):
    board.append([0] * (dx + 1))
  for (pos, vel) in data:
    board[pos[1] - my][pos[0] - mx] = 1
  for y in range(dy+1):
    print(''.join(map(lambda c: ' ' if c == 0 else 'X', board[y])))



def parse_line(input):
  # position=< 21518, -21209> velocity=<-2,  2>
  # print(input)
  pos, vel = input.split('> velocity=<')
  pos = tuple(int(i) for i in pos.replace('position=<', '').split(', '))
  vel = tuple(int(i) for i in vel.replace('>', '').split(', '))
  return (pos, vel)


def parse_input(input):
  input = input.split('\n')
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
position=< 9,  1> velocity=< 0,  2> 
position=< 7,  0> velocity=<-1,  0>  
position=< 3, -2> velocity=<-1,  1>  
position=< 6, 10> velocity=<-2, -1>  
position=< 2, -4> velocity=< 2,  2>  
position=<-6, 10> velocity=< 2, -2>  
position=< 1,  8> velocity=< 1, -1>  
position=< 1,  7> velocity=< 1,  0>  
position=<-3, 11> velocity=< 1, -2>  
position=< 7,  6> velocity=<-1, -1>  
position=<-2,  3> velocity=< 1,  0>  
position=<-4,  3> velocity=< 2,  0>  
position=<10, -3> velocity=<-1,  1>  
position=< 5, 11> velocity=< 1, -2>  
position=< 4,  7> velocity=< 0, -1>  
position=< 8, -2> velocity=< 0,  1>  
position=<15,  0> velocity=<-2,  0>  
position=< 1,  6> velocity=< 1,  0>  
position=< 8,  9> velocity=< 0, -1>  
position=< 3,  3> velocity=<-1,  1>  
position=< 0,  5> velocity=< 0, -1>  
position=<-2,  2> velocity=< 2,  0>  
position=< 5, -2> velocity=< 1,  2>  
position=< 1,  4> velocity=< 2,  1>  
position=<-2,  7> velocity=< 2, -2>  
position=< 3,  6> velocity=<-1, -1> 
position=< 5,  0> velocity=< 1,  0>  
position=<-6,  0> velocity=< 2,  0>  
position=< 5,  9> velocity=< 1, -2>  
position=<14,  7> velocity=<-2,  0>  
position=<-3,  6> velocity=< 2, -1> 
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
