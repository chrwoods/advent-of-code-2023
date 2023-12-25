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


file = open("input/t17f.txt", "r")
score = 0
grid = []

for i, line in enumerate(file.readlines()):
    line = line.strip()
    grid.append([int(x) for x in line])

n, m = dims(grid)

unvisited = set()
shortest_path = {}
prev = {}
for i in range(n):
    for j in range(m):
        for d in range(4):
            shortest_path[(i, j, d)] = 10 ** 10
            unvisited.add((i, j, d))
#
# def get_edges_v0(node):
#     i, j, d = node
#     edges = []
#     ds = [(d + 1) % 4, (d - 1) % 4]
#     dist = 0
#     for _ in range(3):
#         for d2 in ds:
#             i2 = i + d4[d2][0]
#             j2 = j + d4[d2][1]
#             if 0 <= i2 < n and 0 <= j2 < m:
#                 dist2 = dist + grid[i2][j2]
#                 edges.append(((i2, j2, d2), dist2))
#
#         i += d4[d][0]
#         j += d4[d][1]
#         if not 0 <= i < n or not 0 <= j < m:
#             break
#         dist += grid[i][j]
#     return edges

def get_edges(node):
    i, j, d = node
    edges = []
    ds = [(d + 1) % 4, (d - 1) % 4]
    dist = 0
    for _ in range(3):
        i += d4[d][0]
        j += d4[d][1]
        if not 0 <= i < n or not 0 <= j < m:
            return edges
        dist += grid[i][j]
    for _ in range(10 - 3):
        for d2 in ds:
            i2 = i + d4[d2][0]
            j2 = j + d4[d2][1]
            if 0 <= i2 < n and 0 <= j2 < m:
                dist2 = dist + grid[i2][j2]
                edges.append(((i2, j2, d2), dist2))

        i += d4[d][0]
        j += d4[d][1]
        if not 0 <= i < n or not 0 <= j < m:
            break
        dist += grid[i][j]
    return edges

# shortest_path[(0, 0, 0)] = 0
# shortest_path[(0, 0, 1)] = 0

shortest_path[(0, 1, 0)] = grid[0][1]
# shortest_path[(1, 0, 1)] = grid[1][0]


while unvisited:
    cur = None
    for node in unvisited:
        if not cur or shortest_path[node] < shortest_path[cur]:
            cur = node
    if shortest_path[cur] == 10 ** 10:
        break

    neighbors = get_edges(cur)
    for neighbor in neighbors:
        nx, dist = neighbor
        tentative = shortest_path[cur] + dist
        if tentative < shortest_path[nx]:
            shortest_path[nx] = tentative
            prev[nx] = cur


    unvisited.remove(cur)

for d in range(4):
    print(shortest_path[(n - 1, m - 1, d)])

# post DFS
ret = 10 ** 10
endpoint = None
for d in [0, 1]:
    i = n - 1
    j = m - 1
    # ret = min(ret, shortest_path[(i, j, d)])
    dist = grid[i][j]

    for _ in range(2):
        i -= d4[d][0]
        j -= d4[d][1]
        if not 0 <= i < n or not 0 <= j < m:
            break
        dist += grid[i][j]
    for _ in range(7):
        i -= d4[d][0]
        j -= d4[d][1]
        if not 0 <= i < n or not 0 <= j < m:
            break
        # ret = min(ret, shortest_path[(i, j, d)] + dist)
        if shortest_path[(i, j, d)] + dist < ret:
            ret = shortest_path[(i, j, d)] + dist
            endpoint = (i, j, d)
        dist += grid[i][j]

print('sol', ret)

for k, v in shortest_path.items():
    print(k, v)

outgrid = make_empty_grid(lambda: '.', 2, n, m)
cur = endpoint
while cur:
    outgrid[cur[0]][cur[1]] = '>v<^'[cur[2]]
    cur = prev.get(cur)

print_grid(outgrid)

print('sol', ret)