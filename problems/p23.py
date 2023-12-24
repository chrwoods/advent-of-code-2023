import bisect
import collections
import functools
from os import truncate
import regex as re
from collections import defaultdict as dd

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

file = open("input/t23.txt", "r")
score = 0
grid = []

for idx, line in enumerate(file.readlines()):
  line = line.strip()
  grid.append(list(line))

n, m = dims(grid)


def reduce(i, j, n, m):
  if grid[i][j] == '#':
    return False
  if not 1 <= i < n - 1 or not 1 <= j < m - 1:
    return False
  neighbors = [grid[i + x][j + y] for x, y in d4]
  pound_count = 0
  for b in neighbors:
    if b == '#':
      pound_count += 1
  if pound_count == 3:
    grid[i][j] = '#'
    for d in range(4):
      x, y = d4[d]
      if grid[i + x][j + y] != '#':
        reduce(i + x, j + y, n, m)
    return True
  return False


print(n, m)

found = True
while found:
  found = False
  for i in range(1, n - 1):
    for j in range(1, m - 1):
      if i == 1 and j == 1:
        continue
      if i == n - 2 and j == m - 2:
        continue
      found = found or reduce(i, j, n, m)

print_grid(grid)


def get_neighbors(i, j):
  return [((i + x, j + y), grid[i + x][j + y]) for x, y in d4]


cur = (1, 1)
seen = {cur}
path = [cur]
crux = []
end = (n - 2, m - 2)
while True:
  # while grid[cur[0]][cur[1]] == 'v>^<':
  #   d = '>v<^'.index(grid[cur[0]][cur[1]])
  #   cur = (cur[0] + d4[d][0], cur[1] + d4[d][1])
  #   path.append(cur)
  #   seen.add(cur)

  if cur == end:
    # print('end of path', len(path))
    score = max(score, len(path))
    if not crux:
      break
    stop_at, nx = crux.pop()
    while path[-1] != stop_at:
      seen.remove(path.pop())
    cur = nx[0]
    path.append(cur)
    seen.add(cur)
    if len(nx) > 1:
      crux.append((stop_at, nx[1:]))
    continue
  neighbors = get_neighbors(*cur)
  neighbors = [(a, b) for a, b in neighbors if b != '#' and a not in seen]
  n2 = []
  for a, b in neighbors:
    # i, j = cur
    # x, y = a
    # if b == 'v' and x < i:
    #   continue
    # if b == '<' and j < y:
    #   continue
    # if b == '^' and x > i:
    #   continue
    # if b == '>' and y < j:
    #   continue
    n2.append(a)
  neighbors = n2
  if len(neighbors) > 1:
    crux.append((cur, neighbors[1:]))
    cur = neighbors[0]
    path.append(cur)
    seen.add(cur)
  elif len(neighbors) == 1:
    cur = neighbors[0]
    path.append(cur)
    seen.add(cur)
  else:
    # print(cur, 'WHAT THE FUCK')
    # break
    if not crux:
      break
    stop_at, nx = crux.pop()
    while path[-1] != stop_at:
      seen.remove(path.pop())
    cur = nx[0]
    path.append(cur)
    seen.add(cur)
    if len(nx) > 1:
      crux.append((stop_at, nx[1:]))
    if len(crux) < 10:
      print('cruxes', len(crux))

print(score + 1)
