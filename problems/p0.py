import bisect
import collections
import functools
import regex as re
from collections import defaultdict as dd
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


def get_nums(a, split_char=' '):
  return [int(x.strip()) for x in a.split(split_char)]


# find leftmost true (assumming F, F, T, T)
def bin_search(test, a, b):
  while a < b:
    m = (a + b) // 2
    if test(m):
      b = m
    else:
      a = m + 1
  return a


# nums = re.findall('(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)|([0-9]{1})', line, overlapped=True)
# a = word_to_num([num for num in nums[0] if num][0])

file = open("input/t0.txt", "r")
score = 0

for i, line in enumerate(file.readlines()):
  line = line.strip()
  # line = ' '.join(line.split()[2:])

  temp = 0
  score += temp

print(score)

print(make_empty_grid(list, 3, 2, 1, 3))

print(bin_search(lambda x: x > -1, 0, 5))
