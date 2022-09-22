import hashlib

input = open('input.txt', 'r').read().strip()

i = 1
while True:
  row = input + str(i)
  digest = hashlib.md5(row).hexdigest()
  if digest.startswith("00000"):
    print i
    exit()
  i += 1