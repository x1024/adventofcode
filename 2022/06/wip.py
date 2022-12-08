input = open('input.txt', 'r').read().strip()
size = 4
print(min(i+size for i in range(len(input)) if len(set(input[i:i+size])) == size))
size = 14
print(min(i+size for i in range(len(input)) if len(set(input[i:i+size])) == size))