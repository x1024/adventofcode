def easy(input):
  m = len(input)
  n = len(input[0])
  def isVisible(x, y):
    t = input[x][y]
    good = True
    for j in range(0, x):
      if input[j][y] >= t: good = False
    if good: return True
    good = True
    for j in range(x + 1, m):
      if input[j][y] >= t: good = False
    if good: return True
    good = True
    for j in range(0, y):
      if input[x][j] >= t: good = False
    if good: return True
    good = True
    for j in range(y + 1, m):
      if input[x][j] >= t: good = False
    if good: return True
    return False

  return sum(isVisible(x, y) for x in range(m) for y in range(n))


def hard(input):
  m = len(input)
  n = len(input[0])

  def score(x, y):
    t = input[x][y]

    total = 1
    j = x - 1
    seen = 0
    while j >= 0:
      if input[j][y] >= t:
        seen += 1
        break
      if input[j][y] < t: seen += 1
      j -= 1
    total *= seen

    seen = 0
    j = x + 1
    while j < m:
      if input[j][y] >= t:
        seen += 1
        break
      if input[j][y] < t: seen += 1
      j += 1
    total *= seen

    seen = 0
    j = y - 1
    while j >= 0:
      if input[x][j] >= t:
        seen += 1
        break
      if input[x][j] < t: seen += 1
      j -= 1
    total *= seen

    seen = 0
    j = y + 1
    while j < n:
      if input[x][j] >= t:
        seen += 1
        break
      if input[x][j] < t: seen += 1
      j += 1
    total *= seen

    return total

  return max(score(x, y)
    for x in range(m)
    for y in range(n))


input = open('input.txt', 'r').read().strip()
input = [list(map(int, row)) for row in input.split("\n") if row]
print(easy(input))
print(hard(input))