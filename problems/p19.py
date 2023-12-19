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


file = open("input/t19t.txt", "r")
score = 0
grid = []

rules = {}

while True:
    line = file.readline().strip()
    if not line:
        break

    name, parts = line.split('{')
    parts = parts[:-1]
    parts = parts.split(',')
    base = parts[-1]
    parts = parts[:-1]
    subrules = []
    for part in parts:
        a, d = part.split(':')
        if '<' in a:
            b = -1
            a, c = a.split('<')
        else:
            b = 1
            a, c = a.split('>')
        c = int(c)
        subrules.append((a, b, c, d))
    rules[name] = (subrules, base)

class Bound:
    a0 = None
    a1 = None
    b0 = None
    b1 = None

class Xmas:
    def __init__(self):
        self.x = []
        self.m = []
        self.a = []
        self.s = []
    #     self.x = Bound()
    #     self.m = Bound()
    #     self.a = Bound()
    #     self.s = Bound()

bounds = {}
good = {'A', 'R'}
keys = rules.keys()
for key in rules:
    bounds[key] = Xmas()

for key in keys:
    subrules, base = rules[key]
    if all(s[3] in good for s in subrules) and base in good:
        for a, b, c, d in subrules:


print(bounds)