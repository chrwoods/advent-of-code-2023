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

file = open("input/t13.txt", "r")
score = 0
grid = []

for idx, line in enumerate(file.readlines()):
    line = line.strip()
    if not line:
        for xx in range(2):
            n = len(grid)
            go = True
            for i in range(n - 1):
                a, b = i, i + 1
                diffs = 0
                while 0 <= a and b < n:
                    diffs += sum(1 if a != b else 0 for a, b in zip(grid[a], grid[b]))
                    a -= 1
                    b += 1
                if diffs == 1:
                    score += (i + 1) * (1 if xx else 100)
                    go = False
                    break
            if not go:
                break
            grid = transpose(grid)
        grid = []
    else:
        grid.append(list(line))
    
print(score)