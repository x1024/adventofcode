import pprint
import collections
import numpy


class Dir(object):
  all_dirs = []

  def __init__(self, name, parent = None):
    self.name = name
    self.parent = parent
    self.dirs = {}
    self.files = {}
    Dir.all_dirs.append(self)

  def __str__(self):
    path = []
    p = self
    while p:
      path.append(p.name)
      p = p.parent
    path = '/'.join(path[::-1])
    if not path: path = '/'
    return '<Dir path: %s, size: %s>' % (path, self.size())
  
  def size(self):
    return sum(self.files.values()) + sum(d.size() for d in self.dirs.values())

def solve(data):
  # pprint.pprint(data)
  dirs = collections.defaultdict(lambda: 0)
  dir = Dir('')
  files = {}
  for row in data:
    if row[0] == '$':
      command = row[1]
      # print(command)
      print(dir)
      if command == 'ls':
        pass
      else:
        arg = row[2]
        if arg == '/':
          while dir.parent:
            dir = dir.parent
        elif arg == '..':
          dir = dir.parent
        else:
          if arg not in dir.dirs:
            dir.dirs[arg] = Dir(arg, dir)
          dir = dir.dirs[arg]
        # print("\t" * len(dir), command, arg, dir)
        # print("\t" * len(dir), dir)
    elif row[0] == 'dir':
      # dir
      pass
      # print(row)
    else:
      size = int(row[0])
      filename = row[1]
      dir.files[filename] = size

  MAX = 100000
  print("--------")
  total = 0
  for dir in Dir.all_dirs:
    print(dir)
    s = dir.size()
    if s <= MAX:
      total += s

  pprint.pprint(total)
  return total

def parse_line(data):
  return data.split()


def parse_input(data):
  data = data.split('\n')
  data = [row.strip() for row in data]
  data = [row for row in data if row]
  # data = list(map(int, data))
  data = list(map(parse_line, data))
  return data


def test():
  data = '''
  $ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
  '''
  data = parse_input(data)
  result = solve(data)
  print("Test Result: {}".format(result))
  return


# test()
# exit()
data = open('input.txt', 'r').read().strip()
data = parse_input(data)
result = solve(data)
print("Result: {}".format(result))

import pyperclip
pyperclip.copy(str(result))

