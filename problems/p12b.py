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


file = open("input/t12.txt", "r")
score = 0
grid = []

def is_valid(a, b):
    a = ''.join(a)
    a = [x for x in a.split('.') if x]
    # print(a)
    return len(a) == len(b) and all(len(x) == y for x, y in zip(a, b))

def is_valid_wrap(a, b):
    for i, x in enumerate(a):
        if x == '?':
            return is_valid_wrap(a[:i] + ['.'] + a[i + 1:], b) + is_valid_wrap(a[:i] + ['#'] + a[i + 1:], b)
    return is_valid(a, b)


for i, line in enumerate(file.readlines()):
    line = line.strip()
    a, b = line.split(' ')
    b = get_nums(b, ',')
    a = list(a)
    score += is_valid_wrap(a, b)


# print(is_valid('.###.##.#...', [3, 2, 1]))
# print(is_valid_wrap('.###.##..#...', [3, 2, 1]))
# print(is_valid_wrap('.###.##..##...', [3, 2, 1]))
# print(is_valid_wrap(list('?###????????'), [3, 2, 1]))


print(score)
