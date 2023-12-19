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


def distt(a, b):
    return abs(b[1] - a[1]) + abs(b[0] - a[0])


def rotate_grid_clockwise(grid):
    return transpose(grid[::-1])


def print_grid(grid):
    for row in grid:
        print(''.join(row))

def print_bool_grid(grid):
    for row in grid:
        print(''.join('#' if x else '.' for x in row))

def dims(grid):
    return len(grid), len(grid[0])

d4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]


file = open("input/t18.txt", "r")
score = 0
grid = []

A1, A2 = 0, 0

coords = []
i, j = A1, A2
dm = 'RDLU'

n, m = 0, 0
n0, m0 = 0, 0
per = 0

for _, line in enumerate(file.readlines()):
    line = line.strip()
    draw, meters, c = line.split(' ')
    # c = c[1:-1]
    # d = dm.index(draw)
    c = c[2:-1]
    d = int(c[-1])
    c = c[:-1]
    meters = int(c, 16)
    per += meters
    i += d4[d][0] * meters
    j += d4[d][1] * meters
    # if d == 0:
    #     j += 1
    # if d == 1:
    #     i += 1
    coords.append((i, j))
    print(dm[d], meters)

n += 1
m += 1

print(n0, m0)
print(n, m)
#
# grid = make_empty_grid(str, 2, n, m)
# for i, j, c in coords:
#     grid[i][j] = c
#
# q = [(n // 2, m // 2)]
# while q:
#     i, j = q.pop()
#     grid[i][j] = 'seen'
#     for i2 in range(i - 1, i + 2):
#         for j2 in range(j - 1, j + 2):
#             if 0 <= i2 < n and 0 <= j2 < m and (i != i2 or j != j2):
#                 if not grid[i2][j2]:
#                     q.append((i2, j2))
#
#
# print(sum(sum(1 if x else 0 for x in row) for row in grid))

area = 0
for i in range(len(coords)):
    area += (coords[i][0] * coords[i - 1][1]) - (coords[i - 1][0] * coords[i][1])

print(area // 2 + per // 2 + 1)




print(coords)
