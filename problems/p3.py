import collections
import functools
import regex as re
from z3 import *


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


# nums = re.findall('(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)|([0-9]{1})', line, overlapped=True)
# a = word_to_num([num for num in nums[0] if num][0])

file = open("input/t3.txt", "r")
score = 0

grid = []

all_parts = []

for i, line in enumerate(file.readlines()):
  line = line.strip()
  grid.append([x for x in line])

  cur = ''
  for j, c in enumerate(line):
    if c not in '0123456789':
      if cur:
        temp = (cur, i, j - len(cur), j)
        all_parts.append(temp)
        print(temp)
      cur = ''
    else:
      cur += c
  if cur:
    temp = (cur, i, len(line) - len(cur), len(line))
    all_parts.append(temp)
    print(temp)
      
n = len(grid)
m = len(grid[0])

gears = [[[] for _ in range(m)] for _ in range(n)]
# print(grid)
# print(gears)

def is_valid(num, i, j1, j2):
  processed = set()
  for j in range(j1, j2):
    for a in range(-1, 2):
      for b in range(-1, 2):
        # if 0 <= i + a < n and 0 <= j + b < m and grid[i + a][j + b] not in '.0123456789':
          
          # return True
        if 0 <= i + a < n and 0 <= j + b < m and grid[i + a][j + b] == '*':
          if (i + a, j + b) not in processed:
            gears[i + a][j + b].append(int(num))
            processed.add((i + a, j + b))


for num, i, j1, j2 in all_parts:
  # if is_valid(num, i, j1, j2):
    # score += int(num)
  is_valid(num, i, j1, j2)


for i in range(n):
  for j in range(m):
    if len(gears[i][j]) == 2:
      score += gears[i][j][0] * gears[i][j][1]

print(score)
