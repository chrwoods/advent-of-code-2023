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

file = open("input/t25.txt", "r")
score = 0
edges = collections.defaultdict(list)
v = set()
e2 = []

for idx, line in enumerate(file.readlines()):
    line = line.strip()
    a, b = line.split(': ')
    c = b.split(' ')
    v.add(a)
    for d in c:
        # print(a, '->',  d)
        if d == 'nsk':
            continue
        if d == 'zjm':
            continue
        if a == 'jks':
            continue
        e2.append([a, d])
        edges[a].append(d)
        edges[d].append(a)
        v.add(d)

# import graphviz
# dot = graphviz.Digraph(comment='test')
# for a, b in e2:
#     if b == 'nsk':
#         continue
#     if b == 'zjm':
#         continue
#     if a == 'jks':
#         continue
#     dot.edge(a, b)
#     
# dot.render('graphviz-out/bipartite.gv').replace('\\', '/')
    
def full_graph(start):
    q = [start]
    visited = {start}
    while q:
        x = q.pop()
        for e in edges[x]:
            if e not in visited:
                visited.add(e)
                q.append(e)
    return visited

a = full_graph('nmm')
b = full_graph('fbs')

print('zjm' in a)
print('zjm' in b)
print('jks' in a)
print('jks' in b)
print('nsk' in a)
print('nsk' in b)

for x in 'qlg drj tlq rfg'.split(' '):
    print('A' if x in a else 'B')

print()

for x in 'zdf lsg zcp qdz'.split(' '):
    print('A' if x in a else 'B')
    
print((len(a) + 1) * (len(b) + 1))
# print(len(visited))
# print(len(v))
# print(len(visited) * (len(v) - len(visited)))