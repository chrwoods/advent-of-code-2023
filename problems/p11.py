import bisect
import collections
import functools
from os import truncate
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

def transpose(grid):
    return list(zip(*grid))


file = open("input/t11t.txt", "r")
score = 0

grid = []

for i, line in enumerate(file.readlines()):
  line = line.strip()
  grid.append(list(line))


temp = []
rows = []
for i, line in enumerate(grid):
    temp.append(line)
    if all(x == '.' for x in line):
        # temp.append(line)
        rows.append(i)
grid = temp

grid = transpose(grid)

temp = []
cols = []
for i, line in enumerate(grid):
    temp.append(line)
    if all(x == '.' for x in line):
        # temp.append(line)
        cols.append(i)
grid = temp

grid = transpose(grid)

# for line in grid:
#     print(''.join(line))

n, m = len(grid), len(grid[0])

dots = []
for i in range(n):
    for j in range(m):
        if grid[i][j] == '#':
            dots.append((i, j))

def dist(a, b):
    # return abs(b[1] - a[1]) + abs(b[0] - a[0])
    ret = 0
    r1, r2 = min(a[0], b[0]), max(a[0], b[0])
    c1, c2 = min(a[1], b[1]), max(a[1], b[1])
    for i in range(r1, r2):
        ret += 1
        if i in rows:
            ret += (1000000 - 1)
    for i in range(c1, c2):
        ret += 1
        if i in cols:
            ret += (1000000 - 1)
    return ret


xx = len(dots)
for i in range(xx):
    for j in range(i):
        score += dist(dots[i], dots[j])


# print(grid)
print(score)
