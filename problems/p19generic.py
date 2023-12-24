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
    low = None
    high = None


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

# for key in keys:
#     subrules, base = rules[key]
#     if all(s[3] in good for s in subrules) and base in good:
#         outs = []
#         xmas = Xmas()
#         for a, b, c, d in subrules:
#             a =
#

def dfs(cur, constraints):
    def combine_constraints(nx):
        new_cons = []
        for a, b in zip(constraints, nx):
            if a[0] is not None and b[0] is not None:
                i = max(a[0], b[0])
            elif a[0] is not None:
                i = a[0]
            else:
                i = b[0]
            if a[1] is not None and b[1] is not None:
                j = min(a[1], b[1])
            elif a[1] is not None:
                j = a[1]
            else:
                j = b[1]
            new_cons.append([i, j])
        return new_cons

    # print(cur, constraints)
    if cur == 'A':
        # print('im in an A')
        temp = 1
        for j in constraints:
            j0, j1 = j
            if j0 is None:
                j0 = 1
            if j1 is None:
                j1 = 4001
            temp *= j1 - j0

        return max(temp, 0)
    elif cur == 'R':
        return 0

    for j in constraints:
        if j[1] is not None and j[0] is not None and j[1] <= j[0]:
            return 0

    ret = 0
    subrules, base = rules[cur]
    nx = make_empty_grid(lambda: None, 2, 4, 2)
    # print(subrules, base)
    for var, sign, val, dest in subrules:
        # print(var, sign, val, dest)
        v = 'xmas'.index(var)
        if sign < 0:
            if nx[v][1] is not None:
                nx[v][1] = min(nx[v][1], val)
            else:
                nx[v][1] = val
        else:
            if nx[v][0] is not None:
                nx[v][0] = max(nx[v][0], val + 1)
            else:
                nx[v][0] = val + 1
        ret += dfs(dest, combine_constraints(nx))

    for j in constraints:
        if j[1] is not None and j[0] is not None and j[1] <= j[0]:
            return ret

    possible_constraints = []
    for j in constraints:
        if j[1] is not None and j[0] is not None:
            possible_constraints.append([[None, j[0]], [j[1], None]])
        else:
            possible_constraints.append([[j[1], j[0]]])
    for c0 in possible_constraints[0]:
        for c1 in possible_constraints[1]:
            for c2 in possible_constraints[2]:
                for c3 in possible_constraints[3]:
                    ret += dfs(base, [c0, c1, c2, c3])
    return ret


score = dfs('in', make_empty_grid(lambda: None, 2, 4, 2))
print(score)
