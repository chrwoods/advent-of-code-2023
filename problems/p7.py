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

file = open("input/t7.txt", "r")
score = 0

def mapp(card):
  return 'AKQT98765432J'.index(card)

def key_a(hand):
  x = collections.Counter(hand)
  y = sorted([(v, -mapp(k)) for k, v in x.items()], reverse=True)
  return y
# if x[0] == 5:
  #   return ()
  # if x[0] == 4

def sort_key_x(hand):
  hand = hand[0]
  x = key_a(hand)
  if x[0][0] == 5:
    return ('A', -x[0][1])
  if x[0][0] == 4:
    return ('B', -x[0][1], -x[1][1])
  if x[0][0] == 3 and x[1][0] == 2:
    return ('C', -x[0][1], -x[1][1])
  elif x[0][0] == 3:
    return ('D', -x[0][1], -x[1][1], -x[2][1])
  elif x[0][0] == 2 and x[1][0] == 2:
    return ('E', -x[0][1], -x[1][1], -x[2][1])
  elif x[0][0] == 2:
    return ('F', -x[0][1], -x[1][1], -x[2][1], -x[3][1])
  return ('G', -x[0][1], -x[1][1], -x[2][1], -x[3][1], -x[4][1])

def sort_key(new_hand, hand):
  x = key_a(new_hand)
  if x[0][0] == 5:
    return ('A', *[mapp(g) for g in hand])
  if x[0][0] == 4:
    return ('B', *[mapp(g) for g in hand])
  if x[0][0] == 3 and x[1][0] == 2:
    return ('C', *[mapp(g) for g in hand])
  elif x[0][0] == 3:
    return ('D', *[mapp(g) for g in hand])
  elif x[0][0] == 2 and x[1][0] == 2:
    return ('E', *[mapp(g) for g in hand])
  elif x[0][0] == 2:
    return ('F', *[mapp(g) for g in hand])
  return ('G', *[mapp(g) for g in hand])

def sort_key_2(hand):
  hand = hand[0]
  ret = hand
  highkey = sort_key(hand, hand)
  for c in 'AKQT98765432J':
    temp = hand.replace('J', c)
    t2 = sort_key(temp, hand)
    if t2 <= highkey:
      highkey = t2
      ret = temp
  return highkey


hands = []
for i, line in enumerate(file.readlines()):
  line = line.strip()
  hand, bid = line.split(' ')
  hands.append((hand, bid))
  # print(hand, sort_key_2((hand, bid)))

x = sorted(hands, key=sort_key_2)
print(x)

# print(score)

# print(key_a('QQQ53'))
# print(sort_key('KK677'))
# print(sort_key_2(('KK677', 0)))
# print(sort_key_2(('KTJJT', 0)))
# print(mapp('K'))

for i, a in enumerate(reversed(x)):
  # print(i, a[1])
  score += (i  + 1) * int(a[1])

print(score)