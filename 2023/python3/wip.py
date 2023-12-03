import collections
import numpy
import pprint
import re

def main(data):
    data = data.split('\n')
    data = [row.strip() for row in data]
    data = [row for row in data if row]
    data = [row.split() for row in data]
    # data = list(map(int, data))

    result = 0
    print(result)
    return result


data_test = open('input-sample.txt', 'r').read().strip()
result = main(data_test)
print("Test Result: {}".format(result))
result = main(data)

data = open('input.txt', 'r').read().strip()
# pprint.pprint(data)
print("Real Result: {}".format(result))
import pyperclip
pyperclip.copy(str(result))

# import IPython
# IPython.embed()
