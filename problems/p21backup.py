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

file = open("input/t21t.txt", "r")
score = 0
grid = []

rules = {}

for line in file.readlines():
    line = line.strip()
    grid.append(list(line))

n, m = dims(grid)
start = None
for i in range(n):
    if start:
        break
    for j in range(m):
        if grid[i][j] == 'S':
        start = (i, j)
        grid[i][j] = '.'
        break

cur = {start}
for step in range(64):
    nx = set()
    for i, j in cur:
        for dx, dy in d4:
        x, y = i + dx, j + dy
        if x < 0 or x >= n or y < 0 or y >= m:
            continue
        if grid[x][y] == '.':
            nx.add((x, y))
    cur = nx

print(len(cur))
