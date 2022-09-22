input = open('input.txt', 'r').read().strip()

lines = input.split('\n')
distances = {}
cities = set()
for line in lines:
  a, dist = line.split(" = ")
  _from, _to = a.split(" to ")
  distances[(_from, _to)] = int(dist)
  distances[(_to, _from)] = int(dist)
  cities.add(_from)
  cities.add(_to)

import itertools
mindist = 9999999999
for route in itertools.permutations(list(cities)):
  # print route
  total = 0
  for i in range(len(route) - 1):
    _from = route[i]
    _to = route[i+1]
    total += distances[(_from, _to)]
  mindist = min(total, mindist)
  

result = mindist
print("Result: {}".format(result))
