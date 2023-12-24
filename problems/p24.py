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

file = open("input/t24.txt", "r")
score = 0
stones = []

for idx, line in enumerate(file.readlines()):
    line = line.strip()
    a, b = line.split(' @ ')
    stones.append((get_nums(a, ','), get_nums(b, ',')))

vert = 'VERT'

def get_mxb(x, y, x2, y2):
    if x2 == x:
        m = vert
        b = x
    else:
        m = (y2 - y)/(x2 - x)
        b = y - x*(y2 - y)/(x2 - x)
    return (m, b)

def get_mxbs(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (
        get_mxb(x1, y1, x2, y2),
        get_mxb(y1, z1, y2, z2),
        get_mxb(z1, x1, z2, x2),
    )

def get_point(i, fac):
    a, b = stones[i]
    x, y, z = a
    vx, vy, vz = b
    return (x + vx * fac, y + vy * fac, z + vz * fac)

def get_p(p1, p2):
    px, py, pz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
    gc = math.gcd(px, py, pz)
    if gc > 1:
        px //= gc
        py //= gc
        pz //= gc
    return (px, py, pz)

def get_future(p1, pv, factor):
    px, py, pz = p1
    vx, vy, vz = pv
    return (px + vx * factor, py + vy * factor, pz + vz * factor)

def get_sol(p1, p2, factor):
    pv = get_p(p1, p2)
    return get_future(p1, pv, factor)

stones = sorted(stones)
# for i, (a, b) in enumerate(stones):
#     print(i, a, b)

sx0 = Int('sx0')
sy0 = Int('sy0')
sz0 = Int('sz0')
sxv = Int('sxv')
syv = Int('syv')
szv = Int('szv')
equations = []

for i, ((x, y, z), (xv, yv, zv)) in enumerate(stones):
    t = Int(f't{i}')
    equations.append(t >= 0)
    equations.append((x + xv * t) == (sx0 + sxv * t))
    equations.append((y + yv * t) == (sy0 + syv * t))
    equations.append((z + zv * t) == (sz0 + szv * t))
    
solver = Solver()
solver.add(equations)
solver.check()
solved = solver.model()
print(simplify(solved[sx0] + solved[sy0] + solved[sz0]))