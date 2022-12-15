import queue

offset = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

def solve(input):
  data, start, end = input
  routes = bfs([data, end])
  shortest_route = min(val for key, val in routes.items() if data[key[0]][key[1]] == 0)
  return routes[start], shortest_route


def bfs(input):
  data, start = input
  n, m = len(data), len(data[1])
  seen, q = {}, queue.Queue()
  q.put((start, 0))
  seen[start] = 0
  while not q.empty():
    now, steps = q.get()
    height = data[now[0]][now[1]]
    for o in offset:
      new_pos = now[0] + o[0], now[1] + o[1]
      if new_pos in seen: continue
      if not (0 <= new_pos[0] < n) or not (0 <= new_pos[1] < m): continue
      if data[new_pos[0]][new_pos[1]] < height - 1: continue
      q.put((new_pos, steps + 1))
      seen[new_pos] = steps + 1
  return seen


def parse_input(input):
  row_len = input.find("\n") + 1 # Account for the "\n" at the end of the line
  start, end = input.find("S"), input.find("E")
  start = (start // row_len, start % row_len)
  end = (end // row_len, end % row_len)
  data = [
    [ord(col) - ord('a') for col in row]
    for row in input.replace("S", "a").replace("E", "z").split("\n")
  ]
  return data, start, end


input = open('input.txt', 'r').read().strip()
input = parse_input(input)
result = solve(input)
print("Result: {}".format(result))