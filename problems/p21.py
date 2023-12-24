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

def run(steps, start):
    cur = {start}
    for step in range(steps):
        nx = set()
        for i, j in cur:
            for dx, dy in d4:
                x, y = i + dx, j + dy
                if x < 0 or x >= n or y < 0 or y >= m:
                    continue
                if grid[x][y] == '.':
                    nx.add((x, y))
        cur = nx
    return cur

# n0, m0 = n, m
# start = (start[0] + n0 * 4, start[1] + m0 * 4)
# for i in range(n):
#     grid[i] *= 9
# m *= 9
# grid *= 8
# n *= 8
# 
# o = run(23 + n0, start)
# for i in range(n):
#     if i % n0 == 0:
#         print()
#     out = ''
#     for j in range(m):
#         if j % m0 == 0:
#             out += ' '
#         out += 'O' if (i, j) in o else grid[i][j]
#     print(out)
    
goal = 26501365
# goal = 49
# goal = 5 + 11 + 11
test_val = (goal % n) + n * 2

upsize = 7
n0, m0 = n, m
start = (start[0] + n0 * (upsize // 2), start[1] + m0 * (upsize // 2))
grid = [row * upsize for row in grid]
grid *= upsize
n *= upsize
m *= upsize
t9 = make_empty_grid(int, 2, upsize, upsize)
template = run(test_val, start)
for i, j in list(template):
    x = i // n0
    y = j // m0
    t9[x][y] += 1
    
# for i in range(n):
#     if i % n0 == 0:
#         print()
#     out = ''
#     for j in range(m):
#         if j % m0 == 0:
#             out += ' '
#         out += 'O' if (i, j) in template else grid[i][j]
#     print(out)

# 1 5 13 25 41
# 0 4 12 24 40
# 0 1 3 6 10
# x_0 = 1
# x_n = (x_(n - 1)) + 4n
def get_center_num(n):
    return 2 * n * n - 2 * n + 1

# 1: 1 0
# 2: 4 1
# 3: 9 4 = 8 + 1, 4
# 4: 16 9 = 12 + 4, 8 + 1
# 5: 25 16 = 16 + 8 + 1, 12 + 4
# 6: 36 25 = 20 + 12 + 4, 16 + 8 + 1
def get_center_nums_v2(n):
    return n ** 2, (n - 1) ** 2


def get_mult_grid(n):
    size = upsize
    t9m = make_empty_grid(int, 2, size, size)
    mid = size // 2
    # t9m[mid][mid] = get_center_num(n)
    t9m[mid][mid - 1], t9m[mid][mid] = get_center_nums_v2(n)
    t9m[mid - 1][mid - 1] = n - 1
    t9m[mid - 1][mid + 1] = n - 1
    t9m[mid + 1][mid - 1] = n - 1
    t9m[mid + 1][mid + 1] = n - 1
    t9m[mid - 1][mid - 2] = n 
    t9m[mid - 1][mid + 2] = n 
    t9m[mid + 1][mid - 2] = n 
    t9m[mid + 1][mid + 2] = n 
    t9m[0][mid] = 1
    t9m[1][mid] = 1
    t9m[mid][0] = 1
    t9m[mid][1] = 1
    t9m[mid][size - 1] = 1
    t9m[mid][size - 2] = 1
    t9m[size - 1][mid] = 1
    t9m[size - 2][mid] = 1
    return t9m

t9m = get_mult_grid(goal // n0)
for i in range(upsize):
    for j in range(upsize):
        score += t9m[i][j] * t9[i][j]

# print(sum(sum(row) for row in t9))
# print(t9)
# print(t9m)
print(score)
        
    