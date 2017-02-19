import numpy as np
import itertools

import functools

from utils import create_coords_medium

ROWS = 3
COLS = 5

pizza = np.ones((ROWS, COLS), dtype=int)

for x in xrange(1, 4):
    pizza[1][x] = 0

# print 'row', pizza[1,:] # Row
# print 'col', pizza[:,1] # Col
# print 'upper left corner:'
# print pizza[0:2,0:2] # Upper left corner, 2x2

# a = np.arange(225).reshape(15, 15)
a = np.arange(100).reshape(10, 10)
print a

l = []
# for coords in create_coords_medium(a, 12, 4):
for coords in create_coords_medium(a, max_size_of_slice=12, min_ing_per_slice=4):
    l.append(coords)
print 'len', len(l)
for c in l:
    print c
    start_row, start_col, end_row, end_col = c
    print a[start_row:end_row, start_col:end_col]
    print
