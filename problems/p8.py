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


# nums = re.findall('(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)|([0-9]{1})', line, overlapped=True)
# a = word_to_num([num for num in nums[0] if num][0])
# print(make_empty_grid(list, 3, 2, 1, 3))
# print(bin_search(lambda x: x > -1, 0, 5))

file = open("input/t8.txt", "r")
score = 0

moves = file.readline().strip()
file.readline()

edges = {}
for i, line in enumerate(file.readlines()):
  line = line.strip()
  a, b = line.split('=')
  c, d = b[2:-1].split(',')
  edges[a.strip()] = (c.strip(), d.strip())

i = 0
# cur = 'AAA'
# while True:
#   move = moves[i % len(moves)]
#   a, b = edges[cur]
#   # print(cur, move, a, b)
#   if move == 'L':
#     cur = a
#   else:
#     cur = b
#   if cur == 'ZZZ':
#     break
#   i += 1
# print(i + 1)

start_nodes = list(v for v in edges if v[-1] == 'A')
end_nodes = set(v for v in edges if v[-1] == 'Z')
# print(start_nodes)
# print(end_nodes)

# curs = start_nodes
# while True:
#   move = moves[i % len(moves)]
#   nx = set()
#   for cur in curs:
#     a, b = edges[cur]
#     if move == 'L':
#       cur = a
#     else:
#       cur = b
#     nx.add(cur)
#   if all(v[-1] == 'Z' for v in nx):
#     break
#   curs = nx
#   i += 1
# print(i + 1)

# curs = [start_nodes[0]]
# goods = [0]
# while True:
#   move = moves[i % len(moves)]
#   nx = set()
#   for cur in curs:
#     a, b = edges[cur]
#     if move == 'L':
#       cur = a
#     else:
#       cur = b
#     nx.add(cur)
#   if all(v[-1] == 'Z' for v in nx):
#     # print(i + 1)
#     goods.append(i + 1)
#     print(goods[-1] - goods[-2])
#   curs = nx
#   i += 1
# print(i + 1)

goods = [14363, 12737, 16531, 19241, 19783, 11653]

lcm = 9177460370549
print(lcm)
