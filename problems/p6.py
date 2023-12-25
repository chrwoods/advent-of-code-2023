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


# nums = re.findall('(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)|([0-9]{1})', line, overlapped=True)
# a = word_to_num([num for num in nums[0] if num][0])
# cur = [(cur[i], cur[i] + cur[i + 1]) for i in range(0, len(cur), 2)]
# print(make_empty_grid(list, 3, 2, 1, 3))

# ts = [41, 77, 70, 96]
# ds = [249, 1362, 1127, 1011]
# # ts = [7, 15, 30]
# # ds = [9, 40, 200]

# total = 1

# for i in range(len(ts)):
#   t = ts[i]
#   d = ds[i]
#   score = 0
#   for x in range(t + 1):
#     dist = x * (t - x)
#     if dist > d:
#       score += 1
#   print(score)
#   total *= score
# print(total)


t = 41777096
d = 249136211271011

l = 0
r = t

x = (l + r) // 2

def test(m):
  return m * (t - m) > d

a = l
b = x
while a < b:
  m = (a + b) // 2
  if test(m):
    b = m
  else:
    a = m + 1
print(m)

print(test(7206616))
print(test(7206617))
print(test(7206618))

a = x
b = r
while a < b:
  m = (a + b) // 2
  if test(m):
    a = m + 1
  else:
    b = m
print(m)

print(test(34570478))
print(test(34570479))
print(test(34570490))

print(34570478 - 7206617)
