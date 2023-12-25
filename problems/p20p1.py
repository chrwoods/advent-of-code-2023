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

file = open("input/t20.txt", "r")
score = 0
ffd = {}
ffs = {}
cd = {}
cs = {}
broadcaster = []

for idx, line in enumerate(file.readlines()):
    line = line.strip()
    a, b = line.split(' -> ')
    outs = b.split(', ')
    if a == 'broadcaster':
        broadcaster = outs
    elif a[0] == '%':
        ffd[a[1:]] = outs
        ffs[a[1:]] = 0
    elif a[0] == '&':
        cd[a[1:]] = outs
        cs[a[1:]] = {}
    else:
        print('AGH')
        
for c in cs:
    for x, o in ffd.items():
        if c in o:
            cs[c][x] = 0
    for x, o in cs.items():
        if c in o:
            cs[c][x] = 0

pulses = []

def run():
    pulses = [(x, 0, 'broadcaster') for x in broadcaster]
    lows = 1
    highs = 0
    while pulses:
        cur, val, prev = pulses[0]
        pulses = pulses[1:]
        # print(prev, '-high->' if val else '-low->', cur)
        if val:
            highs += 1
        else:
            lows += 1
            
        # memory for conjunctions
        if cur in cs:
            cs[cur][prev] = val
            
        if cur in ffs:
            if not val:
                temp = 1 - ffs[cur]  # invert
                for dest in ffd[cur]:
                    pulses.append((dest, temp, cur))
                ffs[cur] = temp
        elif cur in cs:
            out = 0 if all(cs[cur].values()) else 1
            for dest in cd[cur]:
                pulses.append((dest, out, cur))
        else:
            pass
        
    return lows, highs

a = b = 0
for _ in range(1000):
    l, h = run()
    # print(l, h)
    a += l
    b += h
    
print(a * b)