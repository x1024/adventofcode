input = open('input.txt', 'r').read().strip()
lines = input.split("\n")

letters = 'abcdefghijklmnopqrstuvwxyz'
digraphs = []
trigraphs = []
for i in range(len(letters) - 2):
  trigraphs.append(letters[i:i+3])
for i in range(len(letters)):
  digraphs.append(letters[i] * 2)

def next_str(password):
  i = len(password) - 1
  if password[i] != 'z':
    c = chr(ord(password[i]) + 1)
    return password[:i] + c

  while i >= 0 and password[i] == 'z':
    i -= 1
  c = chr(ord(password[i]) + 1)
  print i
  return password[:i] + c + 'a' * (len(password) - i - 1)



def valid(password):
  i = 0
  found = 0
  while i < len(password) - 1:
    if password[i] == password[i+1]:
      i += 1
      found += 1
    i += 1
  if found < 2:
    return False

  for trigraph in trigraphs:
    if trigraph in password: break
  else:
    return False
  for l in ['i', 'o', 'l']:
    if l in password:
      return False
  return True
  

def solve(input):
  while True:
    # print input
    if valid(input):
      return input
    input = next_str(input)
  

# print valid('hijklmmn')
# print valid('abbceffg')
# print valid('abbcegjk')
# print valid('abcdffaa')

# print solve('abcdefgh')
print solve(input)

result = 0
print("Result: {}".format(result))
