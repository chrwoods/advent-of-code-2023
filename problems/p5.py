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

file = open("input/t5.txt", "r")
score = 0

seeds = file.readline()
seeds = seeds.split(' ')[1:]
file.readline()

maps = []
temp = []

for i, line in enumerate(file.readlines()):
  line = line.strip()
  if not line:
    maps.append(temp)
    temp = []
    continue

  if line[-1] == ':':
    continue

  temp.append(get_nums(line))
maps.append(temp)

# print(maps)

# cur = [int(x) for x in seeds]
# for mp in maps:
#   print(cur)
#   nx = []
#   for x in cur:
#     dest = x
#     for b, a, r in mp:
#       # print(a, x, a + r)
#       if a <= x < a + r:
#         dest = b + (x - a)
#         break
#     nx.append(dest)
#   cur = nx
#   # break

# print(cur)
# print(min(cur))

cur = [int(x) for x in seeds]
cur = [(cur[i], cur[i] + cur[i + 1]) for i in range(0, len(cur), 2)]
# print(cur)
for i, mp in enumerate(maps):
  mp = sorted([(b, a, r) for a, b, r in mp])
  # print()
  # print('mp', mp)
  print('cur', cur)
  nx = []
  for x, y in cur:
    # print()
    # print('x, y:', x, y)
    seed = x
    for a, b, r in mp:
      # print('run', seed, a, b, r)
      # print(a, b, r)
      if a >= y:
        break
      if seed < a:
        nx.append((seed, a))
        seed = a
      start = max(seed, a)
      end = min(y, a + r)
      if start < end:
        nx.append((start + (b - a), end + (b - a)))
      seed = max(seed, end)
      # print('post-run:', nx)
    if seed < y:
      nx.append((seed, y))
    # print('post xy:', nx)
  cur = nx
  # if i:
    # break

print(cur)
print(min(cur))
