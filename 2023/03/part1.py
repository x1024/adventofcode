import collections
import numpy
import pprint
import re

def touches_part(data, x, y):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx >= len(data): continue
            if ny < 0 or ny >= len(data[0]): continue
            if (data[nx][ny] < '0' or data[nx][ny] > '9') and data[nx][ny] != '.':
                return True
    return False

def check(data, used, x,y):
    # print(x, y)
    valid = False
    number = []
    for j in range(y, len(data[0])):
        if data[x][j] < '0' or data[x][j] > '9':
            break
        used.add((x, j))
        number.append(data[x][j])
        if touches_part(data, x, j):
            valid = True

    number = int(''.join(number))
    print(number)
    if valid:
        return int(number)
    return 0

def solve(data):
    result = 0
    used = set()
    # print(data)
    for x in range(len(data)):
        for y in range(len(data[0])):
            if (x,y) in used: continue
            if data[x][y] >= '0' and data[x][y] <= '9':
                result += check(data, used, x, y)
    return result

def main(data):
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    # data = list(map(int, data))

    result = solve(data)
    print(result)
    return result


data = open('input.txt', 'r').read().strip()
data_test = open('input-sample.txt', 'r').read().strip()

result = main(data_test)
print("Test Result: {}".format(result))

result = main(data)
pprint.pprint(data)
print("Real Result: {}".format(result))
# result = main(data)
import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
