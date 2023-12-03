import functools
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
        used[(x, j)] = number
        number.append(data[x][j])
        if touches_part(data, x, j):
            valid = True

    for j in range(y, len(data[0])):
        if data[x][j] < '0' or data[x][j] > '9':
            break
        c = (x, j)
        val = used.get(c, None)
        if val is not None:
            used[c] = int(''.join(number))

    number = int(''.join(number))
    # print(number)
    if valid:
        return int(number)
    return 0

def check2(data, used, x, y):
    numbers = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx >= len(data): continue
            if ny < 0 or ny >= len(data[0]): continue
            number = used.get((nx, ny), None)
            if number is None: continue
            numbers.add(number)
    if len(numbers) == 2:
        return functools.reduce(lambda a, b: a*b, numbers, 1)
    return 0


def solve(data):
    result = 0
    used = {}
    # print(data)
    for x in range(len(data)):
        for y in range(len(data[0])):
            if (x,y) in used: continue
            if data[x][y] >= '0' and data[x][y] <= '9':
                result += check(data, used, x, y)

    result2 = 0
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] == '*':
                print(x, y)
                result2 += check2(data, used, x, y)
            # if (x,y) in used: continue
    return result2

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

# 467835

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
