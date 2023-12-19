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


def roll_rocks_left(grid):
    g2 = []
    for row in grid:
        temp = []
        empty = 0
        rocks = 0
        for c in row:
            if c == '.':
                empty += 1
            elif c == 'O':
                rocks += 1
            else:
                if empty or rocks:
                    temp.extend(['O'] * rocks + ['.'] * empty)
                temp.append('#')
                empty = 0
                rocks = 0
        temp.extend(['O'] * rocks + ['.'] * empty)
        g2.append(temp)
    return g2


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

def full_cycle(grid):
    for _ in range(4):
        grid = roll_rocks_left(grid)
        grid = rotate_grid_clockwise(grid)
    return grid


def get_score(grid):
    score = 0
    n = len(grid)
    for i, row in enumerate(grid):
        # print(''.join(row))
        score += (n - i) * sum(1 if c == 'O' else 0 for c in row)
    return score



file = open("input/t14.txt", "r")
score = 0
grid = []

for i, line in enumerate(file.readlines()):
    line = line.strip()
    grid.append(list(line))

for _ in range(3):
    grid = rotate_grid_clockwise(grid)


for i in range(1000000000):
    grid = full_cycle(grid)

    print(i + 1, get_score(rotate_grid_clockwise(grid)))


grid = rotate_grid_clockwise(grid)
print_grid(grid)


print(score)

# there is a cycle every 28 tries
# 664 is same mod as 1000000000
# 664 is 104619
