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

file = open("input/t22.txt", "r")
score = 0
grid = []

rules = {}


def brick_it(brick):
  a, b, c = brick[0]
  x, y, z = brick[1]
  brick = set()
  for i in range(min(a, x), max(a, x) + 1):
    for j in range(min(b, y), max(b, y) + 1):
      for k in range(min(c, z), max(c, z) + 1):
        brick.add((i, j, k))
  return brick


tower = set()


def try_fall_brick(brick):
  brick_down = set()
  for x, y, z in brick:
    if z == 1 or (x, y, z - 1) in tower:
      return None
    brick_down.add((x, y, z - 1))
  return brick_down


bricks = []
temp_bricks = []

for idx, line in enumerate(file.readlines()):
  line = line.strip()
  x, y = line.split('~')
  temp_brick = (get_nums(x, ','), get_nums(y, ','))
  temp_bricks.append(temp_brick)

temp_bricks.sort(key=lambda x: (x[0][2], x[1][2]))

for temp_brick in temp_bricks:
  brick = brick_it(temp_brick)

  while True:
    next_brick = try_fall_brick(brick)
    if not next_brick:
      break
    # print(idx, 'fell')
    brick = next_brick
  tower.update(brick)
  bricks.append(brick)

# for brick in bricks:
#   print(try_fall_brick(brick))

coord_map = {}
for i, brick in enumerate(bricks):
  for coord in brick:
    coord_map[coord] = i

cannot_delete = set()

brick_map = collections.defaultdict(set)
for i, brick in enumerate(bricks):
  for x, y, z in brick:
    brick_below_idx = coord_map.get((x, y, z - 1))
    if brick_below_idx is not None and brick_below_idx != i:
      brick_map[i].add(brick_below_idx)
  if len(brick_map[i]) == 1:
    cannot_delete.update(brick_map[i])

# print(brick_map)

# for i in range(len(bricks)):
#   if {i} not in brick_map.values():
#     print(chr(ord('A') + i))
#     score += 1
# print(score)

# hiccups = {}

# for i in range(len(bricks)):
#   for j in range(i + 1, len(bricks)):
#     if i in brick_map[j] and j in brick_map[i]:
#       # print(i, j)
#       # hiccups.append({i, j})
#       hiccups[i] = j
#       hiccups[j] = i

# for i in range(len(bricks)):
#   for j in range(i + 1, len(bricks)):
#     for k in range(j + 1, len(bricks)):
#       if i in brick_map[j] and j in brick_map[i]:
#         if i in brick_map[k] and k in brick_map[i]:
#           if j in brick_map[k] and k in brick_map[j]:
#             print(i, j, k)
#         # # hiccups.append({i, j})
#         # hiccups[i] = j
#         # hiccups[j] = i

#   if {i} not in brick_map.values():
#     print(chr(ord('A') + i))
#     score += 1

# ret = set(list(range(len(bricks))))
# for i, x in brick_map.items():
#   if len(x) == 1:
#     a = x.pop()
#     if a in ret:
#       ret.remove(a)
#   elif len(x) == 2 and hiccups.get(i) in x:
#     x.remove(hiccups[i])
#     a = x.pop()
#     if a in ret:
#       ret.remove(a)

# print(len(ret))

print(len(bricks) - len(cannot_delete))

for x in cannot_delete:
  fall = {x}
  while True:
    nx = set()
    for i in range(len(bricks)):
      if i in fall:
        continue
      need_gone = brick_map[i]
      if need_gone and need_gone <= fall:
        nx.add(i)
    if not nx:
      break
    fall.update(nx)
  # print('run', x, len(fall) - 1)
  score += len(fall) - 1

print(score)
