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


def dist(a, b):
    return abs(b[1] - a[1]) + abs(b[0] - a[0])


def rotate_grid_clockwise(grid):
    ret = []
    # return list(zip(*[line for line in grid]))[::-1]
    return transpose(grid[::-1])


def print_grid(grid):
    for row in grid:
        print(''.join(row))

def print_bool_grid(grid):
    for row in grid:
        print(''.join('#' if x else '.' for x in row))


file = open("input/t16t.txt", "r")
score = 0
grid = []

for i, line in enumerate(file.readlines()):
    line = line.strip()
    grid.append(list(line))

n, m = len(grid), len(grid[0])

d4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# def dfs(i, j, d):
#     print(i, j, d)
#     if not 0 <= i < n:
#         return
#     if not 0 <= j < m:
#         return
#     energized[i][j] = 1
#     c = grid[i][j]
#     if c == '\\':
#         d = [1, 0, 3, 2][d]
#     elif c == '/':
#         d = [3, 2, 1, 0][d]
#     elif c == '|':
#         if d in [0, 2]:
#             d = 1
#             dfs(i + d4[d][0], j + d4[d][1], d)
#             d = 3
#             dfs(i + d4[d][0], j + d4[d][1], d)
#         return
#     elif c == '-':
#         if d in [1, 3]:
#             d = 0
#             dfs(i + d4[d][0], j + d4[d][1], d)
#             d = 2
#             dfs(i + d4[d][0], j + d4[d][1], d)
#         return
#     return dfs(i + d4[d][0], j + d4[d][1], d)

def get_score(x1, x2, x3):
    energized = make_empty_grid(int, 2, n, m)
    q = [(x1, x2, x3)]
    seen = set()
    x = 0
    def add_q(a):
        if a not in seen:
            q.append(a)
            seen.add(a)

    while q:
        i, j, d = q.pop()
        x += 1
        # if x > 1000:
        #     break
        if not 0 <= i < n:
            continue
        if not 0 <= j < m:
            continue
        energized[i][j] = 1
        c = grid[i][j]
        # print(i, j, c, d, len(q))
        # print(q)
        if c == '\\':
            d = [1, 0, 3, 2][d]
        elif c == '/':
            d = [3, 2, 1, 0][d]
        elif c == '|':
            if d in [0, 2]:
                d = 1
                add_q((i + d4[d][0], j + d4[d][1], d))
                d = 3
                add_q((i + d4[d][0], j + d4[d][1], d))
                continue
        elif c == '-':
            if d in [1, 3]:
                d = 0
                # print('x', i, d4[d][0], j, d4[d][1])
                add_q((i + d4[d][0], j + d4[d][1], d))
                d = 2
                # print('x', i, d4[d][0], j, d4[d][1])
                add_q((i + d4[d][0], j + d4[d][1], d))
                continue
        add_q((i + d4[d][0], j + d4[d][1], d))
    return sum(sum(row) for row in energized)

score = 0
for i in range(n):
    score = max(score, get_score(i, 0, 0), get_score(i, m - 1, 2))
for i in range(m):
    score = max(score, get_score(0, i, 1), get_score(n-1, i, 3))

print(get_score(0, 0, 0))
print(score)


