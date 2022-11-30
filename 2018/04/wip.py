import pprint
import collections
import numpy

AWAKE = 0
ASLEEP = 1

def solve(input):
  # pprint.pprint(input)
  data = {}
  last_sleep = -1
  for row in input:
    date = row[0]
    minute = int(row[1].split(":")[1])
    msg = row[2]
    if msg == 'falls asleep':
      last_sleep = minute
    elif msg == 'wakes up':
      if date not in data[id]:
        data[id][date] = {}
      # print(date, last_sleep, minute)
      for x in range(last_sleep, minute):
        data[id][date][x] = True
    else:
      id = int(msg.split()[1].strip('#'))
      last_sleep = -1
      if id not in data:
        data[id] = {}
  
  most_sleep_count = 0
  result = False
  for id in data:
    sleeps = collections.Counter()
    for day in data[id]:
      sleeps.update(data[id][day])
    print(id, len(sleeps))
    if not sleeps: continue
    minute, count = sleeps.most_common(1)[0]
    print(id, minute, count, most_sleep_count)
    if count > most_sleep_count:
      most_sleep_count = count
      result = (id, minute, count)

  (id, minute, count) = result
  return id * minute


def parse_line(input):
  row = input.replace("[", "").replace("]", "").split()
  r = row[0], row[1], ' '.join(row[2:])
  # print(r)
  return r


def parse_input(input):
  input = input.split('\n')
  input = list(sorted(input))
  input = [row.strip() for row in input]
  input = [row for row in input if row]
  # input = list(map(int, input))
  input = list(map(parse_line, input))
  return input


def test():
  input = '''
[1518-11-01 00:00] Guard #10 begins shift  
[1518-11-01 00:05] falls asleep            
[1518-11-01 00:25] wakes up                
[1518-11-01 00:30] falls asleep            
[1518-11-01 00:55] wakes up                
[1518-11-01 23:58] Guard #99 begins shift  
[1518-11-02 00:40] falls asleep            
[1518-11-02 00:50] wakes up                
[1518-11-03 00:05] Guard #10 begins shift  
[1518-11-03 00:24] falls asleep            
[1518-11-03 00:29] wakes up                
[1518-11-04 00:02] Guard #99 begins shift  
[1518-11-04 00:36] falls asleep            
[1518-11-04 00:46] wakes up                
[1518-11-05 00:03] Guard #99 begins shift  
[1518-11-05 00:45] falls asleep            
[1518-11-05 00:55] wakes up                
  '''
  input = parse_input(input)
  result = solve(input)
  print("Test Result: {}".format(result))
  return


# test()
input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))
