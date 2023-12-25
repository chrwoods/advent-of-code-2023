import collections
import functools
import regex as re
from z3 import *

file = open("input/t1.txt", "r")
score = 0

# for line in file.readlines():
#   line = line.strip()
#   nums = [c for c in line if c in '1234567890']
#   score += int(nums[0] + nums[-1])

# for line in file.readlines():
#   line = line.strip()
#   nums = [c for c in line if c in '1234567890']
#   score += int(nums[0] + nums[-1])

def word_to_num(word):
  map = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
  }
  return str(map.get(word, word))

for i, line in enumerate(file.readlines()):
  line = line.strip()
  nums = re.findall('(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)|([0-9]{1})', line, overlapped=True)
  a = word_to_num([num for num in nums[0] if num][0])
  b = word_to_num([num for num in nums[-1] if num][0])

  temp = int(a + b)
  print(i, line, temp)
  score += temp


print(score)
