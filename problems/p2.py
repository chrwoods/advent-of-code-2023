import collections
import functools
import regex as re
from z3 import *


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


# nums = re.findall('(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)|([0-9]{1})', line, overlapped=True)
# a = word_to_num([num for num in nums[0] if num][0])

file = open("input/t2.txt", "r")
score = 0

for i, line in enumerate(file.readlines()):
  line = line.strip()

  game = ' '.join(line.split()[2:])
  possible = True
  rounds = game.split(';')
  total = {'red': 0, 'green': 0, 'blue': 0}
  for round in rounds:
    acc = collections.defaultdict(int)
    parts = round.split(',')
    for part in parts:
      a, b = part.strip().split(' ')
      acc[b] += int(a)
    for key in total:
      total[key] = max(total[key], acc[key])
  temp = 1
  for key in total:
    temp *= total[key]

  score += temp
    
  # if possible:
  #   score += i + 1

print(score)
