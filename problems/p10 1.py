import bisect
import collections
import functools
import math
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

file = open("input/t10.txt", "r")
score = 0
grid = []

for idx, line in enumerate(file.readlines()):
    line = line.strip()
    grid.append(list(line))
    
n, m = dims(grid)


def new_dir(c, d):
    if c == '.':
        return -1
    elif c == '|':
        if d in [1, 3]:
            return d
        return -1
    elif c == '-':
        if d in [0, 2]:
            return d
        return -1
    elif c == 'L':
        if d == 1:
            return 0
        if d == 2:
            return 3
        return -1
    elif c == 'J':
        if d == 0:
            return 3
        if d == 1:
            return 2
        return -1
    elif c == '7':
        if d == 0:
            return 1
        if d == 3:
            return 2
        return -1
    elif c == 'F':
        if d == 2:
            return 1
        if d == 3:
            return 0
        return -1
    else:
        print('AGH')

start = None
for i in range(n):
    if start:
        break
    for j in range(m):
        if grid[i][j] == 'S':
            start = (i, j)
            break

for s in '|-LJ7F':
    i, j = start
    grid[i][j] = s
    d = 0
    if s in '|J':
        d = 3
    elif s == '7':
        d = 1
        
    path = [start]
    i += d4[d][0]
    j += d4[d][1]
    while 0 <= i < n and 0 <= j < m and (i, j) != start:
        d = new_dir(grid[i][j], d)
        if d < 0:
            break
        path.append((i, j))
        i += d4[d][0]
        j += d4[d][1]
    if (i, j) == start and new_dir(s, d) >= 0:
        print(s)
        print(len(path))
        print(len(path) // 2)
        break

outgrid = make_empty_grid(lambda: ' ', 2, n, m)
for i, j in path:
    # outgrid[i][j] = '#'
    outgrid[i][j] = grid[i][j]

print_grid(outgrid)

visited = {(0, 0)}
q = [(0, 0)]
outgrid[0][0] = '#'
while q:
    i, j = q.pop()
    for x, y in d4:
        i2, j2 = i + x, j + y
        if 0 <= i2 < n and 0 <= j2 < m and (i2, j2) not in visited:
            # visited.add((i2, j2))
            if outgrid[i2][j2] == '.':
                outgrid[i2][j2] = '#'
                visited.add((i2, j2))
                q.append((i2, j2))
                
# print_grid(outgrid)
 
print(sum(sum(1 if c == '.' else 0 for c in row) for row in outgrid))