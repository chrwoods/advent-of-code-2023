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


def get_score(grid):
    score = 0
    n = len(grid)
    for i, row in enumerate(grid):
        # print(''.join(row))
        score += (n - i) * sum(1 if c == 'O' else 0 for c in row)
    return score

def hash_alg(part):
    cur = 0
    for c in part:
        cur += ord(c)
        cur *= 17
        cur %= 256
    return cur


file = open("input/t15.txt", "r")
score = 0

line = file.readline().strip()
parts = line.split(',')
# for part in parts:
    # cur = 0
    # for c in part:
    #     cur += ord(c)
    #     cur *= 17
    #     cur %= 256
    # score += cur
    #

boxes = [list() for _ in range(256)]

for part in parts:
    if part[-1] == '-':
        label = part[:-1]
        box = hash_alg(label)
        boxes[box] = [x for x in boxes[box] if x[0] != label]
    else:
        label, b = part.split('=')
        b = int(b)
        box = hash_alg(label)
        replaced = False
        for i in range(len(boxes[box])):
            if boxes[box][i][0] == label:
                boxes[box][i] = (label, b)
                replaced = True
                break
        if not replaced:
            boxes[box].append((label, b))

for box in range(256):
    for i in range(len(boxes[box])):
        score += (box + 1) * (i + 1) * boxes[box][i][1]

print(score)



