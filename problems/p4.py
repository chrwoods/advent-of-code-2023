import collections
import functools
import regex as re
from z3 import *

DIGITS_CHARS = '0123456789'


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


def make_empty_grid(factory, dimensions, *sizes):
  if dimensions == 0:
    return factory()
  return [
      make_empty_grid(factory, dimensions - 1, *(sizes[1:]))
      for _ in range(sizes[0])
  ]


# nums = re.findall('(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)|([0-9]{1})', line, overlapped=True)
# a = word_to_num([num for num in nums[0] if num][0])

# print(make_empty_grid(list, 3, 2, 1, 3))

file = open("input/t4.txt", "r")
score = 0

n = 202
num_cards = [1] * n

for i, line in enumerate(file.readlines()):
  line = line.strip()

  cards = ' '.join(line.split()[2:])
  a, b = cards.split('|')
  winning = {int(x.strip()) for x in b.split()}
  lotto = [int(x.strip()) for x in a.split()]

  matches = 0
  for x in lotto:
    if x in winning:
      matches += 1

  for j in range(i + 1, i + matches + 1):
    if j < n:
      num_cards[j] += num_cards[i]

print(sum(num_cards))
