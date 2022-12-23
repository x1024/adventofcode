import re

def binsearch(callback, start = 0, step = 1 << 64):
  while step > 0: start, step = (start + step * callback(start + step)), step >> 1
  return start

code = ('\n'.join(['def ' + re.sub("([a-z]{4})", "\\1()", row).replace(":", ": return") for row in open('input2.txt', 'r').read().split('\n') if row]))
code_part_2 = re.sub("(def root\(\): return ([a-z]{4})\(\) (\+|\-|\*|\/) ([a-z]{4})\(\))", "\\1\ndef root_part_2(): return \\2() > \\4()", code).replace("/", "//")
open("helper.py", "w").write(code_part_2)
import helper

print(helper.root())

helper_input = 0
def humn(): return helper_input
helper.humn = humn

def binsearch_cb(value):
  global helper_input
  helper_input = value
  return helper.root_part_2()

print(binsearch(binsearch_cb) + 1)